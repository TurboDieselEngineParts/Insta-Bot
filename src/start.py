import os
from datetime import datetime
import random
from time import sleep
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium_stealth import stealth

# ---------- Setup ----------
# Create images directory if it doesn’t already exist
os.makedirs("images", exist_ok=True)

# ---------- Configuration ----------
CHROMEDRIVER_PATH = "/opt/homebrew/bin/chromedriver"
USERNAME = "info@connectionsphere.co.uk"
PASSWORD = "London728678!"
HASHTAG_LIST = ["LondonArchitecture"]
AVG_ACTIONS_PER_HOUR = 3
ACTIVE_HOURS = (8, 22)  # Active between 8am and 10pm


# ---------- Helper Functions ----------
def wait_for_element(driver, by, value, timeout=15):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )


def wait_and_click(driver, by, value, timeout=15):
    elem = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))
    elem.click()
    return elem


def poisson_delay(avg_actions_per_hour):
    rate_per_min = avg_actions_per_hour / 60.0
    delay_minutes = np.random.exponential(1 / rate_per_min)
    return delay_minutes * 60  # seconds


def is_active_hour(active_hours):
    now = datetime.now().hour
    return active_hours[0] <= now < active_hours[1]


def random_comment():
    comments = ["Really cool!", "Nice work :)", "Nice gallery!!", "So cool! :)"]
    return random.choice(comments)


def type_like_human(element, text):
    for char in text:
        element.send_keys(char)
        sleep(random.uniform(0.05, 0.15))


# ---------- Main Bot Function ----------
def run_instabot():
    service = Service(executable_path=CHROMEDRIVER_PATH)
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("start-maximized")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(service=service, options=options)

    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    try:
        driver.implicitly_wait(5)
        driver.get("https://www.instagram.com/accounts/login/")
        sleep(random.uniform(2, 5))

        # Accept cookies if prompted
        try:
            cookie_btn = driver.find_element(
                By.XPATH,
                "/html/body/div[3]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]",
            )
            ActionChains(driver).move_to_element(cookie_btn).pause(
                random.uniform(0.5, 1.5)
            ).click().perform()
        except Exception:
            pass

        # Login form
        username_input = driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/div/div/div[1]/div[2]/div/form/div[1]/div[1]/div/label/input",
        )
        type_like_human(username_input, USERNAME)
        password_input = driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/div/div/div[1]/div[2]/div/form/div[1]/div[2]/div/label/input",
        )
        type_like_human(password_input, PASSWORD)

        driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/div/div/div[1]/div[2]/div/form/div[1]/div[3]",
        ).click()
        sleep(random.uniform(5, 8))

        # Save login info
        try:
            save_info_btn = driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div/section/div/button",
            )
            ActionChains(driver).move_to_element(save_info_btn).pause(
                random.uniform(0.5, 1.5)
            ).click().perform()
        except Exception:
            pass
        sleep(random.uniform(2, 4))

        # Notifications
        try:
            notif_btn = driver.find_element(
                By.XPATH,
                "/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]",
            )
            ActionChains(driver).move_to_element(notif_btn).pause(
                random.uniform(0.5, 1.5)
            ).click().perform()
        except Exception:
            pass
        sleep(random.uniform(2, 4))

        # Load followed user list
        try:
            prev_user_list = pd.read_csv("users_followed_list.csv").iloc[:, 1].tolist()
        except Exception:
            prev_user_list = []

        new_followed, followed, likes, comments = [], 0, 0, 0

        for hashtag in HASHTAG_LIST:
            if not is_active_hour(ACTIVE_HOURS):
                print("Outside active hours. Sleeping for 10 minutes.")
                sleep(600)
                continue

            driver.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
            sleep(random.uniform(4, 7))

            try:
                first_thumbnail = driver.find_element(
                    By.XPATH,
                    "/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div[2]",
                )
                ActionChains(driver).move_to_element(first_thumbnail).pause(
                    random.uniform(0.5, 1.5)
                ).click().perform()
            except Exception as e:
                print(f"💥 Failed to click first thumbnail: {e}")
                continue
            sleep(random.uniform(2, 4))

            for _ in range(2):
                try:
                    username = driver.find_element(
                        By.XPATH,
                        "/html/body/div[5]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div[1]/div/div/span/span/span/div/div/a/div",
                    ).text
                    print(f"Username: {username}")

                    now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"images/{username}_{now_str}.png"
                    driver.save_screenshot(filename)

                    if username not in prev_user_list:
                        print(f"Unseen: {username}")

                        follow_btn = driver.find_element(
                            By.XPATH,
                            "/html/body/div[5]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div[2]/button/div/div",
                        )
                        print(f"Follow button text: {follow_btn.text}")

                        if follow_btn.text == "Follow":
                            ActionChains(driver).move_to_element(follow_btn).pause(
                                random.uniform(0.5, 1.5)
                            ).click().perform()
                            new_followed.append(username)
                            followed += 1
                            print(f"✔️ Followed {username}")

                            # Like
                            button_like = driver.find_element(
                                By.XPATH,
                                "/html/body/div[5]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[1]/span[1]/div",
                            )
                            ActionChains(driver).move_to_element(button_like).pause(
                                random.uniform(0.5, 1.5)
                            ).click().perform()
                            likes += 1
                            print("❤️ Liked the post")
                            sleep(random.randint(18, 25))

                            # Comment with some probability
                            comm_prob = random.randint(1, 10)
                            if comm_prob > 7:
                                comments += 1
                                try:
                                    driver.find_element(
                                        By.XPATH,
                                        "/html/body/div[3]/div[2]/div/article/div[2]/section[1]/span[2]/button/span",
                                    ).click()
                                    comment_box = driver.find_element(
                                        By.XPATH,
                                        "/html/body/div[3]/div[2]/div/article/div[2]/section[3]/div/form/textarea",
                                    )
                                    type_like_human(comment_box, random_comment())
                                    sleep(1)
                                    comment_box.send_keys(Keys.ENTER)
                                    print("💬 Commented")
                                    sleep(random.randint(22, 28))
                                except Exception:
                                    print("⚠️ Failed to comment.")

                    # Next post
                    driver.find_element(By.LINK_TEXT, "Next").click()
                    sleep(random.randint(20, 25))

                except Exception as e:
                    print(f"❌ Error during post interaction: {e}")
                    break

        prev_user_list.extend(new_followed)
        pd.DataFrame(prev_user_list).to_csv("users_followed_list.csv")
        print(f"\n✅ Liked {likes} photos.")
        print(f"✅ Commented on {comments} posts.")
        print(f"✅ Followed {followed} new users.")

    finally:
        driver.quit()
        print("🚪 Browser closed.")


if __name__ == "__main__":
    run_instabot()
