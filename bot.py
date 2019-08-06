import time
import math
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, InvalidSelectorException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

class Dailies_Bot:
    def __init__(self, loginInfo):
        """
        Initializes the webdriver & logs into Neopets
        """
        self.itemsCollected = 0
        self.badItemWords = ['Old', 'Kelp', 'Algae', 'Fern', 
                             'Rockfish', 'Sludge', 'Rotting', 
                             'Petrified', 'Reject', 'Von Roo', 
                             'Forgotten Shore', 'Tiki Tack Keyring', 
                             'Krawk Pirate Ship', 'Broken Toy Sailboat', 
                             'Pencil Sharpener', 'Cinder Block', 'Pirate Attack',
                             'Shiny Obsidian', 'Barbed Wire', 'Rotten', 'Broken',
                             'Tin Can', 'Sandals'
                            ]

        options = webdriver.ChromeOptions()
        #i dont think this works for turning on flash
        prefs = {
            "profile.default_content_setting_values.plugins": 1,
            "profile.content_settings.plugin_whitelist.adobe-flash-player": 1,
            "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 1,
            "PluginsAllowedForUrls": "http://www.neopets.com/faerieland/wheel.phtml"
        }
        
        options.add_experimental_option("prefs", prefs)
        
        #actual start of webdriver setup above doesn't seem to work
        self.driver = webdriver.Chrome('/Users/jihimc18/Downloads/chromedriver', options=options)
        self.driver.get('http://www.neopets.com/login')
        
        loginLink = '//*[@id="header"]/table/tbody/tr[1]/td[3]/a[1]' #xpath only way all others fail
        self.driver.find_element_by_xpath(loginLink).click()

        usernameField = "/html/body[@id='neobdy']/div[@id='main']/div[@id='content']/table/tbody/tr/td[@class='content']/div[@class='welcomeContent']/div[@class='welcomeLogin']/form/div[@class='welcomeLoginContent']/div[@class='welcomeLoginUsername']/div[@class='welcomeLoginUsernameInput']/input"
        passwordField = "/html/body[@id='neobdy']/div[@id='main']/div[@id='content']/table/tbody/tr/td[@class='content']/div[@class='welcomeContent']/div[@class='welcomeLogin']/form/div[@class='welcomeLoginContent']/div[@class='welcomeLoginPassword']/div[@class='welcomeLoginPasswordInput']/input"

        self.driver.find_element_by_xpath(usernameField).send_keys(loginInfo[0])
        self.driver.find_element_by_xpath(passwordField).send_keys(loginInfo[1], Keys.RETURN)
    
    def loopMoneyTree(self, info):
        """
        Runs the searchMoneyTree() method until claim limit, 
        
        To determine the claim limit, the method uses either its own counter
        (if the player did not collect any items prior to running the bot) or by 
        determining if a stylistic difference in "Oops!" appears: when the player
        reaches claim limit, then the "oops" text is centered instead of being on left.
        
        Parameters
        ----------
        info : tuple(nameOfDailyStr, linkToDailyStr, xpathToDaily)
            See description for doADaily().
        
        Returns
        -------
        str
            At function's end, you will have reached claim limit.
        """
        hitLimitString = None
        while (self.itemsCollected < 10 and hitLimitString is None):
            try:
                print(self.searchMoneyTree(info))
                hitLimitString = self.driver.find_element_by_xpath("/html/body[@id='neobdy']/div[@id='main']/div[@id='content']/table/tbody/tr/td[@class='content']/div[2]/center[1]/p").text
            except NoSuchElementException:
                #Kinda hacky design: if we can't detect the center version of "oops",
                #we know claim limit hasn't been hit, so the find_element abovee will throw
                #NoSuchElementException, meaning we should keep going to get more items, hence the pass.
                
                #When we do find center "oops" via xpath, then the hitLimitString will
                #no longer be none, meaning we've got our 10 items and should exit the loop.
                pass
        self.driver.quit()
        return "You've hit the daily limit!"
              
    def searchMoneyTree(self, info):
        """
        Performs a single runthrough of the Money Tree. 
        
        It searches for either the first item that does NOT contain words indicative
        of rubbish OR it refreshes continuously looking for the occasional NC/NP/Rare items donation.
        
        Parameters
        ----------
        info : tuple(nameOfDailyStr, linkToDailyStr, xpathToDaily)
            See description for doADaily().
        
        Returns
        -------
        str
            There are 3 possible strings that can be returned, based on the following situations:
            1) A failure message if the bot wasn't able to grab an item fast enough
            2) A success message if the bot successfully grabs it
            3) A warning message if MT has all bad items/the ghost took everything.
        """
        self.driver.get(info[1])
        numOfItems = len(self.driver.find_elements_by_xpath(info[2] + '/tbody/tr/td')) #counts how many td's to determine item count
        #print(numOfItems)
        for row in range((numOfItems // 6) + 1):
            for col in range(((numOfItems - row * 6) % 7) if (row == (numOfItems // 6)) else 6): 
                itemXpath = info[2] + '/tbody/tr[' + str(row + 1) + ']/td[' + str(col + 1) + ']/div[@class="donated"]'
                itemName = self.driver.find_element_by_xpath(itemXpath + "/p[@class='name']").text
                if (not any(nopeWord in itemName for nopeWord in self.badItemWords)):
                    #cycles through the td's if any contains a nopeWord (useless item), skipped over
                    #print(self.driver.find_element_by_xpath(itemXpath).text)
                    self.driver.find_element_by_xpath(itemXpath + "/a").click()
                    #refers to actual clickable image of item
                    if ("Oops" in self.driver.find_element_by_xpath("/html/body[@id='neobdy']").text):
                        return("Darn! Could not get " + itemName)
                    else:
                        self.itemsCollected = self.itemsCollected + 1
                        return ("Success! You got" + itemName + ". This is item #" + str(self.itemsCollected))
        return ("All the items in MT are shitty :(, or the ghost took everything")
        #print(numOfItems)
        #print(self.driver.find_element_by_xpath(item[2]).text)
    
    def trudys(self, info):
        self.driver.get(info[1])
        countTextElement = self.driver.find_element_by_xpath("/html/body[@id='neobdy']/div[@id='main']/div[@id='content']/table/tbody/tr/td[@class='content']/div[2]/div[@class='count_down_box']/p[@class='trudy_count_text']")
        
        action = webdriver.common.action_chains.ActionChains(self.driver)
        width = countTextElement.size['width']
        height = countTextElement.size['height']
        print(str(width) + " " + str(height))
        
        action.move_to_element_with_offset(countTextElement, width/2, -110)
        action.click()
        action.perform()
        self.driver.sleep(6)
    
    def doADaily(self, info, f = None):
        """
        handles a daily, be it single click or more advanced ones 
        
        Parameters
        ----------
        info : tuple(nameOfDailyStr, linkToDailyStr, xpathToDaily)
            Takes in relevant information about the daily.
            1) nameOfDailyStr refers to the name of the daily (e.g. Money Tree)
            2) linkToDailyStr represents the link to the daily (e.g. neopets.com/freebies)
            3) xpathToDaily is the xpath to the button that submits the daily
        
        f : str, optional
            A string that has the same name as one of Dailies-Bot's method, for 
            special cases when the daily is multi-step.
        """
        
        if f is not None:
            return getattr(self, f)(info)
        else:
            try:
                self.driver.get(info[1])
                self.driver.find_element_by_xpath(info[2]).click()
                
                if (info[0] == "Trudys"):
                    self.driver.sleep(10)
                #OMELETTEE & JELLY WORLD ERRORS
                if ("NO! You cannot take more than" in self.driver.find_element_by_xpath("/html/body[@id='neobdy']").text):
                    return ("You've already collected from " + info[0])  

                #OBSIDIAN QUARRY ERROR
                elif ("What do you think you're doing" in self.driver.find_element_by_xpath("/html/body[@id='neobdy']").text):
                    return "You've already collected from Obsidian Quarry"

                #MONTHLY FREEBIE ERROR
                elif ("Oops" in self.driver.find_element_by_xpath("/html/body[@id='neobdy']").text):
                    return "You've already collected your monthly freebie"

                #SHOP OF OFFER ERROR    
                elif ("Something has happened" not in self.driver.find_element_by_xpath("/html/body[@id='neobdy']").text and info[0] == "Shop of Offers"):
                    return "You've already collected from Shop of Offers"
                else:
                    return ("Success collecting from " + info[0])
            except NoSuchElementException:
                return ("You've already collected from " + info[0] +"!!!")
    
    def findPrice(self, item, numTries, pricing, sensitivity, amountOff):
        """
        Finds the price of one item 
        
        Parameters
        ----------
        item: str
            The Neopets item in question.
            
        numTries: int
            Determines how many Shop Wizard searches for the given item
            
        pricing: str
            Determines how you want the item to be priced. There are 3 possible values:
            1) "lowest" is by default; findPrice will find the lowest price for your item over all numTries search.
            2) "average" adds up all the unweighted prices and averages them for a single search; that average is then added to the averages
                from the other numTries - 1 searches
            3) "undercut" works the same as lowest, except the lowest price found is then reduced by amountOff percent OR by just amountOff.
            
        sensitivity: double
            Prevents super cheap/super expensive prices from ruining calculations; set at 0.3 by default. Given 0 < sensitivity < 1, sensitivity has different uses
            depending on what "pricing" is selected:
            1) If "pricing" is set as "lowest" or "undercut", then sensitivity will IGNORE the cheapest item found in a given search IF the cheapest item's price is more than
            (sensitivity * 100%) lower than the 2nd cheapest item's price. I.e. if cheapestItemPrice < (1 - sensitivity) * 2ndCheapestItemPrice, then cheapestItemPrice will be ignored.
            2) If "pricing" is set as "average," then any price < (1 - sensitivity) * 2ndCheapestItemPrice or any price > (1 + sensitivity) * 2ndCheapestItemPrice will not be included
            in the average calculations.
            
        amountOff: int or double
            Applicable ONLY IF "undercut" is inputted for "pricing"; set at 150 by default. AmountOff determines what fraction BELOW (if 0 < amountOff < 1)
            or how much NP below (if amountOff >= 1) the lowest price found your item should be.
            e.g. if amountOff = 0.1 and the lowest price was 100 NP, then the method returns 90 NP for your item price
            if amountOff = 20 and lowest price was 100, then method returns 80 NP.
            
        Returns
        -------
        int
            Returns the local variable currentPrice, which represents the determined price of your item.
        
        """
        currentPrice = 0  
        totalNumOfResults = 0
        print(item) 
        
        for i in range(numTries):
            if (i == 0):
                self.driver.get("http://www.neopets.com/market.phtml?type=wizard")
                #changes search criteria to exact so no potentially name overlaps
                select = Select(self.driver.find_element_by_xpath("/html/body[@id='neobdy']/div[@id='main']/div[@id='content']/table/tbody/tr/td[@class='content']/div[2]/div[@class='contentModule']/table[@class='contentModuleTable']/tbody/tr[2]/td[@class='contentModuleContent']/div/table/tbody/tr/td[2]/form/table/tbody/tr[3]/td[2]/select"))
                select.select_by_value("exact")
                self.driver.find_element_by_xpath("/html/body[@id='neobdy']/div[@id='main']/div[@id='content']/table/tbody/tr/td[@class='content']/div[2]/div[@class='contentModule']/table[@class='contentModuleTable']/tbody/tr[2]/td[@class='contentModuleContent']/div/table/tbody/tr/td[2]/form/table/tbody/tr[1]/td[2]/input").send_keys(item, Keys.RETURN)
            else:
                self.driver.refresh() #we can simply refresh search results if it's not our first time visiting        
            try:
                tempPrice = int(self.driver.find_element_by_xpath("/html/body[@id='neobdy']/div[@id='main']/div[@id='content']/table/tbody/tr/td[@class='content']/div[2]/table[2]/tbody/tr[2]/td[4]").text.replace(' NP', '').replace(',', ''))
                #the 2nd cheapest item this search
                tempPrice2 = int(self.driver.find_element_by_xpath("/html/body[@id='neobdy']/div[@id='main']/div[@id='content']/table/tbody/tr/td[@class='content']/div[2]/table[2]/tbody/tr[3]/td[4]").text.replace(' NP', '').replace(',', ''))
                #the cheapest item this search

                if (pricing == "lowest" or pricing == "undercut"):   
                    #the abs is meant to protect against one-off super cheap items: as long as the cheapest item isn't 30%+ cheaper than 2nd item, then one-off probably not anomaly.
                    #for example, sometimes ppl get frozen years ago and sell shit super cheap by today's standard. 
                    if (currentPrice == 0 or (tempPrice < currentPrice and abs((tempPrice2 - tempPrice) / tempPrice2) < sensitivity)):
                        currentPrice = tempPrice
                elif (pricing == "average"):
                    trCount = len(self.driver.find_elements_by_xpath("/html/body[@id='neobdy']/div[@id='main']/div[@id='content']/table/tbody/tr/td[@class='content']/div[2]/table[2]/tbody/tr"))
                    for i in range(trCount - 1):
                        tempCurrentPrice = int(self.driver.find_element_by_xpath("/html/body[@id='neobdy']/div[@id='main']/div[@id='content']/table/tbody/tr/td[@class='content']/div[2]/table[2]/tbody/tr[" + str(i + 2) + "]/td[4]").text.replace(' NP', '').replace(',', ''))              
                        if (not (tempCurrentPrice < ((1 - sensitivity) * tempPrice2)) and not (tempCurrentPrice > ((1 + sensitivity ) * tempPrice2))):
                            currentPrice += tempCurrentPrice
                            totalNumOfResults += 1
                        elif (tempCurrentPrice > tempPrice2):
                            break
                else:
                    return "Invalid pricing input."
            except NoSuchElementException:
                print("No results found in Shop Wizard")
                pass
            
        if (pricing == "lowest"):         
            print(currentPrice)
            return currentPrice
        elif (pricing == "average"):
            print(currentPrice // totalNumOfResults)
            return currentPrice // totalNumOfResults
        elif (pricing == "undercut"):
            if (amountOff < 1):
                print(math.floor(currentPrice * (1 - amountOff)))
                return(math.floor(currentPrice * (1 - amountOff)))
            else:
                print (math.floor(currentPrice - amountOff))
                return math.floor(currentPrice - amountOff)
    
    
    def priceShopItems(self, numTries = 5, pricing = "lowest", sensitivity = 0.3, amountOff = 100):
        """
        Sets all shop items with a price determined by findPrice.
        
        Warning: while most prices determined by this function, regardless of the "pricing" option, are accurate,
        this is still an algorithm, so be sure double-check on any particularly valuable items in case something went haywire.
        
        Parameters
        ----------
        numTries, optional: int
            See findPrice for detailed description.
        
        pricing, optional: str
            See findPrice for detailed description.
        
        sensitivity, optional: double
            See findPrice for detailed description.
        
        amountOff, optional: int or double
            See findPrice for detailed description.
        
        Returns
        -------
        List
            Returns local variable priceList, which is a List containing all the prices for all the items in your shop, in order.
        """
        
        self.driver.get("http://www.neopets.com/market.phtml?type=your")
        itemRowXpath = "/html/body[@id='neobdy']/div[@id='main']/div[@id='content']/table/tbody/tr/td[@class='content']/form/table/tbody/tr"
        numOfRows = len(self.driver.find_elements_by_xpath(itemRowXpath)) - 2
        itemList = []
        priceList = []
        itemQuantities = []
        
        for row in range(numOfRows):
            itemList.append(self.driver.find_element_by_xpath(itemRowXpath + "[" + str(row + 2) + "]/td[1]").text)
            itemQuantities.append(int(self.driver.find_element_by_xpath(itemRowXpath + "[" + str(row + 2) + "]/td[3]").text))
        print(itemList)
        for item in itemList:      
            priceList.append(self.findPrice(item, numTries, pricing, sensitivity, amountOff))
              
        self.driver.get('http://www.neopets.com/market.phtml?type=your')
        for row in range(numOfRows):
            self.driver.find_element_by_xpath(itemRowXpath + "[" + str(row + 2) + "]/td[5]/input").send_keys(priceList[row])
        print(sum([price * quantity for price, quantity in zip(priceList, itemQuantities)]))
        
        self.driver.quit()
        return priceList
    
    if __name__ == "__main__":
        return; #power users, maybe open up ipython shell?
    else:
        pass #probably should open up the gui for user friendliness

