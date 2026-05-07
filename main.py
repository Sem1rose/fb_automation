import time
import json
import random
from playwright.sync_api import sync_playwright

def human_type(element, text):
    for char in text:
        element.type(char)
        time.sleep(random.uniform(0.05, 0.15))

def switch_profile(page, profile_name):
    print(f"Attempting to switch to: {profile_name}")
    try:
        profile_menu = page.locator('//div[@aria-label="Your profile" or @aria-label="ملف الشخصي" or @aria-label="Account"]')
        profile_menu.click()
        time.sleep(2)
        
        quick_target = page.get_by_text(profile_name, exact=True).first
        
        if quick_target.is_visible():
            print(f"Found {profile_name} in quick menu. Clicking...")
            quick_target.click()
        else:
            see_all = page.get_by_text("See all profiles") or page.get_by_text("عرض كل الملفات الشخصية")
            if see_all.is_visible():
                see_all.click()
                time.sleep(2)
                page.get_by_text(profile_name, exact=True).first.click()
            else:
                print(f"Could not find switcher for {profile_name}")
                page.keyboard.press("Escape")
                return False

        print(f"Switch initiated. Waiting for reload...")
        time.sleep(8)
        return True
            
    except Exception as e:
        print(f"Switching failed: {e}")
        page.keyboard.press("Escape")
        return False

def run_automation():
    with open('tasks.json', 'r', encoding='utf-8') as f:
        tasks = json.load(f)
        
    with sync_playwright() as p:
        user_data_dir = "./user_data"
        
        context = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            args=["--start-maximized"],
            no_viewport=True
        )
        
        page = context.pages[0] 
            
        for task in tasks:
            print(f"\n--- Starting Task: {task['profile_name']} ---")
            
            page.goto("https://www.facebook.com")
            time.sleep(4)
            
            try:
                current_id = page.locator('//div[@aria-label="Your profile" or @aria-label="Account"]').get_attribute('aria-label')
                if task['profile_name'].lower() in str(current_id).lower():
                    print(f"Already active as {task['profile_name']}. Skipping switch.")
                else:
                    switch_profile(page, task['profile_name'])
            except:
                switch_profile(page, task['profile_name'])
            
            print(f"Navigating to post: {task['post_url']}")
            page.goto(task['post_url'])
            page.wait_for_load_state('domcontentloaded')
            time.sleep(5)
            
            try:
                like_btn = page.get_by_label("Like", exact=False).first or page.get_by_label("أعجبني", exact=False).first
                if like_btn and like_btn.is_visible():
                    like_btn.click()
                    print("Successfully Liked!")
                
                comment_box = page.get_by_role("textbox", name="Comment") or page.get_by_role("textbox", name="اكتب تعليقًا")
                if comment_box and comment_box.is_visible():
                    comment_box.click()
                    human_type(comment_box, task['comment_text'])
                    comment_box.press("Enter")
                    print(f"Commented: '{task['comment_text']}'")
                else:
                    print("Warning: Comment box not found on this post.")

            except Exception as e:
                print(f"Post interaction failed: {e}")
            
            print(f"Waiting {task['delay']} seconds...")
            time.sleep(task['delay'])
        
        print("\nAll tasks completed!")
        context.close()
   
if __name__ == "__main__":
    run_automation()