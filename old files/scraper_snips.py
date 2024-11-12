#Snippets of code that can be used in scraper if necessary

tripTypePath = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[1]/div"
tripTypeButton = driver.find_element(By.XPATH, tripTypePath)
tripTypeButton.click()

oneWayPath = "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[1]/div/div/div/div[2]/ul/li[2]"
oneWayButton = driver.find_element(By.XPATH, oneWayPath)
oneWayButton.click()


    # ss.filteredTrips = []
    # st.code(ss.travelData)
    # if st.button('show trips'): 
    #     for i in range(len(dates)):
    #         sourceA = ss.travelData[0]['trips'][i]['details']
    #         sourceB = ss.travelData[1]['trips'][i]['details']
    #         for tripA in sourceA:
    #             for tripB in sourceB:
    #                 if tripA['destination'] == tripB['destination']:
    #                     j = 0
    #                     for j in range(len(ss.filteredTrips)):
    #                         totalPrice = 0
    #                         for trip in ss.filteredTrips[j]['trips']:
    #                             totalPrice += trip['price']
    #                         if totalPrice > tripA['price'] + tripB['price']:
    #                             break
    #                     ss.filteredTrips.insert(j, 
    #                     {
    #                         'dates': dates[i],
    #                         'destination': tripA['destination'],
    #                         'trips': [{
    #                                     'source': ss.travelData[0]['sourceAirport'],
    #                                     'price': tripA['price']
    #                                 },
    #                                 {
    #                                     'source': ss.travelData[1]['sourceAirport'],
    #                                     'price': tripB['price']
    #                                 }]
    #                     })

    #     st.code(ss.filteredTrips)