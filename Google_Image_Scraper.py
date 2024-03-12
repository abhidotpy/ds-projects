'''
Scrap images from images.google.com for the given prompt using selenium

Date: 10-02-2024
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from numpy import ravel
import matplotlib.pyplot as plt
from PIL import Image
import io, base64
import traceback

sources = []
k, limit = 0, 10
fig, ax = plt.subplots(2, 5)
plt.subplots_adjust(0.01, 0.01, 0.99, 0.99)
ax = ravel(ax)
prompt = "friuts"

# Open the WebDriver instance for the Edge browser. This will let us control the webpage via Edge
options = webdriver.EdgeOptions()
options.add_argument("--headless=True")
driver = webdriver.Edge(options=options)

try:

    # Open the webpage and enter prompt in search bar
    driver.get("https://images.google.com")
    search = driver.find_element(By.NAME, 'q')
    search.send_keys(prompt)

    # Wait max 20s until website has fully loaded. Then click on search button (submit type button)
    driver.execute_script("arguments[0].click()", WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(driver.find_element(By.XPATH, "//button[@type='submit']"))))

    # Now find all image files from the results. They are contained in the image tag
    images = driver.find_elements(By.XPATH, "//div[@class='mJxzWe']/img")

    print(images[3])

    # Pick <limit> image WebElements and extract out image links
    for image in images:
        link = image.get_attribute('src')
        if link == None or link.startswith("https://"):
            pass
        elif k >= limit:
            break
        else:
            sources.append(link)
            k+=1
except:
    traceback.print_exc()
finally:
    driver.quit()

print(sources)
for i, source in enumerate(sources):
    
    # Images are default base64 encoded so decode them using base64decode and pillow to read the final image file
    img = source.split(',')[-1]
    img = Image.open(io.BytesIO(base64.b64decode(img)))

    # Finally display them in the proper axis as image files
    ax[i].imshow(img)
    ax[i].set_axis_off()

plt.show()
