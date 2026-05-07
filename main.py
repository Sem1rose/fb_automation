from playwright.sync_api import sync_playwright
import time

def login_and_save():
    with sync_playwright() as p:
        user_data_dir = "./user_data"
        
        print("Launching browser... Please log in to Facebook manually.")
        
        context = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            args=["--start-maximized"]
        )
        
        page = context.new_page()
        page.goto("https://www.facebook.com")
        
        # The script will stay open for 2 minutes to give you time to log in
        # You can close the browser window manually when you are done
        print("Waiting for you to log in... after you log in, you can close the browser window.")
        time.sleep(120)
        
        context.close()
        
if __name__ == "__main__":
    login_and_save()