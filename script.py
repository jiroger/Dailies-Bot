import bot

myBot = bot.Dailies_Bot(('#', '#'))
fakeClickXpath = "/html/body[@id='neobdy']/div[@id='main']/div[@id='header']/table/tbody/tr[2]/td[@id='navigation']/table/tbody/tr/td[@id='nst']"
#this is so clickable doesent throww invalidselectorexception use this when daily doesent event require a click

bunchOfLinks = [
    #('http://www.neopets.com/soupkitchen.phtml', '/html/body[@id="neobdy"]/div[@id="main"]/div[@id="content"]/table/tbody/tr/td[@class="content"]/div[2]/div[@id="bxwrap"]/div[@class="bx-wrapper"]/div[@class="bx-viewport"]/ul[@id="bxlist"]/li[2]/div/a[1]/img/@src'),
    ('Jelly World','http://www.neopets.com/jelly/jelly.phtml', '//*[@value="Grab some Jelly"]'),
    ('Giant Omelette', 'http://www.neopets.com/prehistoric/omelette.phtml', '//*[@value="Grab some Omelette"]'), 
    ('Bank Interest','http://www.neopets.com/bank.phtml', '//*[@value="Collect Interest"]'), 
    #('Money Tree','http://www.neopets.com/donations.phtml', "/html/body[@id='neobdy']/div[@id='main']/div[@id='content']/table/tbody/tr/td[@class='content']/div[@id='mt-main']/div[@id='mt-container']/div[@id='mt-content']/table", 'loopMoneyTree'),
    
    ('Altador Prizes','http://www.neopets.com/altador/council.phtml?prhv=ddeff7997d56500585c63666ded5fe5e', '//*[@value="Collect your gift"]'), 
    ('Shop of Offers','http://www.neopets.com/shop_of_offers.phtml?slorg_payout=yes', fakeClickXpath), 
    
    ('Monthly Freebies','http://www.neopets.com/freebies', fakeClickXpath),
    ('Obsidian Quarry','http://www.neopets.com/magma/quarry.phtml', fakeClickXpath),
    ('Apple Bobbing','http://www.neopets.com/halloween/applebobbing.phtml?', '//*[@id="bob_button"]'),
    ('Anchor Management','http://www.neopets.com/pirates/anchormanagement.phtml', '//*[@id="btn-fire"]')
]

#notFreeClickables = [
#    ('http://www.neopets.com/prehistoric/mediocrity.phtml','/html/body[@id="neobdy"]/div[@id="main"]/div[@id="content"]/table/tbody/tr/td[@class="content"]/div[2]/embed[@id="flash_23635456827"]'),
#    ('http://www.neopets.com/faerieland/wheel.phtml', "/html/body[@id='neobdy']/div[@id='main']/div[@id='content']/table/tbody/tr/td[@class='content']/div[2]/embed[@id='flash_43066163226']")
#]
# chromee fucking disabled all ways to turn on flash programatically in chrome 71+

#for oneDaily in bunchOfLinks:
    #print(myBot.doADaily(oneDaily))
    
#print(myBot.doADaily(('Money Tree','http://www.neopets.com/donations.phtml', "/html/body[@id='neobdy']/div[@id='main']/div[@id='content']/table/tbody/tr/td[@class='content']/div[@id='mt-main']/div[@id='mt-container']/div[@id='mt-content']/table"), 'loopMoneyTree'))
print(myBot.priceShopItems(numTries = 1, pricing = "undercut"))
#print(myBot.doADaily(('Trudys', 'http://www.neopets.com/trudys_surprise.phtml'), 'trudys'))
