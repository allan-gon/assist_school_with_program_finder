from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep

FROM = "El Camino College"
DEGREE = "Data Science"


def basic_get_and_input_from_school(driver: webdriver) -> None:
    driver.get("https://assist.org/")
    sleep(1)
    from_input = driver.find_element(By.ID, "fromInstitution")
    from_input.send_keys(FROM, Keys.ENTER)


def go_to_school(driver: webdriver, school: str) -> None:
    # TODO: make a more permanent/elegent solution
    # TODO: allows for user input
    while True:
        try:
            basic_get_and_input_from_school(driver)
            to_input = driver.find_element(By.XPATH, '//*[@id="agreement"]')
            to_input.send_keys(school, Keys.ENTER)
            # garbage sometomes works sometimes doesn't
            to_input.send_keys(Keys.ENTER)
            btn = driver.find_element(
                By.XPATH, '//*[@id="transfer-agreement-search"]/div[4]/button'
            )
            btn.click()
            break
        except ElementClickInterceptedException:
            pass


def find_programs(driver: webdriver, school: str) -> list[str]:
    go_to_school(driver, school)
    sleep(1)
    programs = driver.find_elements(By.CLASS_NAME, "viewByRowColText")
    return [program.text for program in programs]


def find_schools_with_agreements(driver: webdriver) -> list[str]:
    basic_get_and_input_from_school(driver)
    to_dropdown = driver.find_elements(By.CLASS_NAME, "ng-input")[2].click()
    sleep(0.5)
    options = driver.find_elements(By.CLASS_NAME, "ng-option")
    return [option.text.split("To: ")[-1] for option in options]


def main() -> None:
    # go to assist
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    transferable_schools = find_schools_with_agreements(driver)

    for school in transferable_schools:
        programs = find_programs(driver, school)
        for program in programs:
            if DEGREE in program:
                with open("./data/results.txt", "a") as file:
                    file.write(f"{school}\n")
                print("Found one")
                break


if __name__ == "__main__":
    main()
