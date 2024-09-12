import requests
from bs4 import BeautifulSoup
import json
import os
import re
import time
from datetime import datetime

def get_soup_object_from_url(url):
    
    #check if we can get the content of the HTML file using the url
    #if we cannot, return an error
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(str(e))
        return {"error": str(e)}

    #get the beautifulSoup object form the response content and return it
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def fetch_reviews_data_from_page(url):

    #get the soup object from the url
    soup = get_soup_object_from_url(url)

    # return an error if soup object was not correctly created
    if (not soup) or ("error" in soup):
        #return "error"
        return soup #maybe to remove back

    # get the HTML tag with JSON informations and convert it into str
    jsons_block = str(soup.find("script", id="__NEXT_DATA__"))
           
    #extract the reviews part from the jsons_block using regex and str replace
    start_pattern ="\"reviews\":"
    end_pattern = ",\"products\"" #test remplacer
    #end_pattern = ",\"filteredReviewMetrics\"" #nouveau end pattern à prendre en compte

    regex = rf"{start_pattern}.*{end_pattern}"
    reviews_block = str(re.search(regex, jsons_block, re.I).group()).\
        replace(start_pattern,"").\
        replace(end_pattern,"")
    
    #convert companies_block into json
    #print (f"reviews_block = {reviews_block}") pour debug
    reviews_json = json.loads(reviews_block)
    
    return reviews_json


def fetch_reviews_data_for_company(company_name_id , output_directory = "data/bank"):
    
    # If the json file already exists we do not start again companies data extraction
    output_json_filename = f'{output_directory}/{company_name_id}_reviews.json'

    #TEST correction to do to the outputput filename if company_name_id containts /
    if company_name_id.find("/") > -1:
        company_name_id2 = company_name_id.replace("/","__")
        output_json_filename = f'{output_directory}/{company_name_id2}_reviews.json'

    #---------------------------------------------------------------------------
    
    # Remove the 3 lines below to scrape each times even if a preexisting review json file exists
    #if os.path.exists(output_json_filename):
    #    print(f"{output_json_filename} already exists.")
    #    return
        
    # Message to indicate the begining of reviews data extraction
    print("*****************************************************************")
    print(f"Reviews data extraction for company_id: {company_name_id}")
    print("*****************************************************************\n\n")

    # measure processing time
    start_time = time.time()
    
    reviews_data = []
    page_number = 1

    #--------------------------------------------
    nb_403_error = 0
    nb_500_error = 0
    #-----------------------------------------------
    #get reviews data from all the page of the defined company
    MAX_PAGE_NUMBER = 10000
    while True and (page_number < MAX_PAGE_NUMBER): #security condition to go out of a potential infinite loop

        #Test to add a sleep of 10 sec 
        if page_number%50 == 0:
            time.sleep(1)
        #else:
        #    time.sleep(1)
        

        #url of the page to be extracted (modification for page_number = 1 case)
        if page_number == 1:
             url = f"https://fr.trustpilot.com/review/{company_name_id}?sort=recency"
        else:
            url = f"https://fr.trustpilot.com/review/{company_name_id}?page={page_number}&sort=recency"

        #get the reviews data from the page
        page_data = fetch_reviews_data_from_page(url)

        #Condition when we ask for a page that does not exist, we are supposed to go out of the loop
        if not page_data or "error" in page_data:
            #--------------------------------------------------------------
            print("page_data =",page_data, " ",("403 Client Error: Forbidden" in str(page_data) ))
            

            if ("403 Client Error: Forbidden" in str(page_data)):
                print("wait 60 sec")
                time.sleep(60)
                nb_403_error+=1

                if nb_403_error > 20:
                    break
                continue

            if ("500 Server Error: Internal" in str(page_data)):
                print("wait 60 sec")
                time.sleep(60)
                nb_500_error+=1

                if nb_500_error > 20:
                    break
                continue
            #--------------------------------------------------------------
            break

        #----------------------------------------
        nb_403_error = 0
        nb_500_error = 0
        #500 Server Error: Internal Server Error
        #------------------------------------------

        # Message to indicate which page is extracted
        print(f"company_id: {company_name_id}  page: {page_number}")
        
        reviews_data.extend(page_data)
        page_number += 1

    #get the current date at format "yyyy:mm-:dTHH:MM:SS.us*3Z"
    date_now = f'{datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]}Z'

    #Build the final json file for reviews data for the company
    final_data = [{
                    "identifyingName" : company_name_id,
                    "extractionDate": date_now,
                    "reviews" : reviews_data
    }]

    
    #Write the results into a json file
    with open(output_json_filename, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)

    end_time = time.time()

    #Message to indicate the end of the process
    print(f"\n\nCompany data extraction time duration : {end_time - start_time} seconds for {page_number-1} pages")
    print(f"Reviews Data extraction for company_id {company_name_id} complete and saved to JSON.")

    return

def fetch_reviews_data_for_all_companies_from_json(companies_json_filename = "data/bank/bank.json", output_directory = "data/bank"):

    
    # If the companies json file does not exists we return
    if not os.path.exists(companies_json_filename):
        print(f"""The companies json does not exists.\n 
        To create it, use the function: \n\nfetch_companies_data_from_category(category ="bank",output_json_filename = "data/bank/bank.json")\n """)
        return

    # Message to indicate the begining of reviews data extraction
    print("===================================================================================")
    print(f"Reviews data extraction for all companies starts:")
    print("===================================================================================\n\n")

    # measure processing time
    start_time = time.time()
    
    # Load the companies json file
    with open(companies_json_filename, 'r', encoding='utf-8') as f:
        companies_json = json.load(f)

    #for each company collect all their reviews which are stored in a json file in the oupt_directory
    for company in companies_json:
        company_name_id = company['identifyingName']
        fetch_reviews_data_for_company(company_name_id = company_name_id , output_directory = output_directory) 


    # measure processing time
    end_time = time.time()
    
    # Message to indicate the begining of reviews data extraction
    print("\n\n===================================================================================")
    print(f"CompleteCompanies data extraction time duration : {end_time - start_time} seconds")
    print(f"Reviews data extraction for all companies ends")
    print("===================================================================================\n\n")
    return


def fetch_company_data_from_page(url):

    #get the soup object from the url
    soup = get_soup_object_from_url(url)

    # return an error if soup object was not correctly created
    if (not soup) or ("error" in soup):
        return "error"

    # get the HTML tag with JSON informations and convert it into str
    jsons_block = str(soup.find("script", id="__NEXT_DATA__"))
           
    #extract the companies part from the json_block using regex and str replace
    start_pattern ="\"businesses\":"
    end_pattern = ",\"totalPages\""

    regex = rf"{start_pattern}.*{end_pattern}"
    companies_block = str(re.search(regex, jsons_block, re.I).group()).\
        replace(start_pattern,"").\
        replace(end_pattern,"")
    
    #convert companies_block into json
    companies_json = json.loads(companies_block)
    
    return companies_json               




def fetch_companies_data_from_category(category ="bank",output_json_filename = "data/bank/bank.json"):

    # Remove the 4 lines below to scrape each times even if a preexisting review json file exists
    #If the json file already exists we do not start again companies data extraction <- not anymore 
    #if os.path.exists(output_json_filename):
    #    print(f"{output_json_filename} already exists.")
    #    return

    
    final_data = []
    page_number = 1
    #get companies data from all the page of the defined category
    MAX_PAGE_NUMBER = 10000
    while True and (page_number < MAX_PAGE_NUMBER): #security condition to go out of a potential infinite loop
        
        url = f'https://fr.trustpilot.com/categories/{category}?page={page_number}'

        #get the companies data from the page
        page_data = fetch_company_data_from_page(url)

        #Condition when we ask for a page that does not exist, we are supposed to go out of the loop
        if not page_data or "error" in page_data:
            break
        final_data.extend(page_data)
        page_number += 1    

    #Write the results into a json file
    with open(output_json_filename, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)
            
    print(f"{category} Companies Data extraction complete and saved to JSON.")


if __name__ == "__main__":
    #test
    print("SCRAPING START")

    # Directory for data storage
    #output_directory = 'data/bank'
    #os.makedirs(output_directory, exist_ok=True)
    
    output_directory_companies = 'data/bank/companies'
    os.makedirs(output_directory_companies, exist_ok=True)
    
    output_directory_reviews = 'data/bank/reviews'
    os.makedirs(output_directory_reviews, exist_ok=True)


    # Define the category of interest
    companies_category = "bank"

    # Define companies form the defined category json output filnname 
    companies_json_filename = f'{output_directory_companies}/{companies_category}.json'

    # Fetch data for all banking companies and write it in a json file
    fetch_companies_data_from_category(category =companies_category,output_json_filename = companies_json_filename)

    # Fetch reviews data for all banking companies and write it in individuals json files
    fetch_reviews_data_for_all_companies_from_json(companies_json_filename = companies_json_filename, output_directory = output_directory_reviews)
