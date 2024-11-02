#Snippets of code that can be used in scraper if necessary

tripTypePath = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[1]/div"
tripTypeButton = driver.find_element(By.XPATH, tripTypePath)
tripTypeButton.click()

oneWayPath = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[1]/div/div/div/div[2]/ul/li[2]"
oneWayButton = driver.find_element(By.XPATH, oneWayPath)
oneWayButton.click()