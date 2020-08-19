from selenium.webdriver.firefox.options import Options as FirefoxOptions
from IsbankSpyder import IsbankSpyder

def make_spyder():
    url = "https://www.isbank.com.tr/en/foreign-exchange-rates"

    special_options = FirefoxOptions()
    special_options.headless = False

    spyder = IsbankSpyder(url=url, options=special_options)

    return spyder


def redirect_message():
    """
    Print message when wrong file is being ran
    """
    print("\n"*3 + "Please launch the file labeled main_script.py" + "\n"*3)


if __name__ == "__main__":
    redirect_message()
