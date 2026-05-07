import time
import json
import random
from playwright.sync_api import sync_playwright
# from playwright_stealth import stealth
# import playwright_stealth

def human_type(element, text):
    for char in text:
        element.type(char)
        time.sleep(random.uniform(0.1, 0.3))  #simulate human typing speed
    
def run_automation():
    with open('tasks.json', 'r', encoding='utf-8') as f:
        tasks = json.load(f)
        
    with sync_playwright() as p:
        user_data_dir = "./user_data"
        
        context = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            args=["--start-maximized"]
        )
        
        page = context.new_page()
        # playwright_stealth.stealth(page)    
            
        for task in tasks:
            print(f"Processing: {task['profile_name']}")
            
            page.goto(task['post_url'])
            page.wait_for_load_state('domcontentloaded')
            time.sleep(5)
            
            try:
                like_btn = page.get_by_label("Like", exact=False).first or page.get_by_label("أعجبني", exact=False).first
                if like_btn and like_btn.is_visible():
                    like_btn.click()
                    print("Clicked Like!")
                
                comment_box = page.get_by_role("textbox", name="Write a comment") or page.get_by_role("textbox", name="اكتب تعليقًا")
                if comment_box and comment_box.is_visible():
                    comment_box.click()
                    human_type(comment_box, task['comment_text'])
                    comment_box.press("Enter")
                    print("Commented!")

            except Exception as e:
                print(f"Error on the Post: {e}")
            
            print(f"Waiting {task['delay']}s before next task...")
            time.sleep(task['delay'])
        
        context.close()
                
if __name__ == "__main__":
    run_automation()