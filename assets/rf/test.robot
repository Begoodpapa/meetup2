*** Settings ***
Documentation    This is a test suite that verifys home page and some key functionalities of Yellow website
Suite Setup    Open Target Website
Suite Teardown    Close Browser  
Library    Screenshot
Library    SeleniumLibrary
Library    YellowCommonLibrary

*** Variables ***
${server}    https://www.yellow.co.nz
${browser}    chrome 
${defaultLocation1}    Town, suburb, city or region
${defaultLocation2}    Auckland
${defaultPrompt}    I'm looking for...
${searchResultKeyText}    View On Wises


*** Test Cases ***
Homepage Function Should Be Available
    [Documentation]    A test case to verify homepage elements and display
    [Setup]    Init Test Dictionary
    Capture Page Screenshot
    Default Text Is Available In Search Bar    ${defaultPrompt}
    Default Text Is Available In Location
    Region List Should Be Available When Click The City Name    ${regionList}
    Input A Keyword For Search
    Validate Search Result Page Elements

*** Keywords ***
Open Target Website
    #Set Selenium Speed    0.5 seconds
    Open Browser    ${server}    ${browser}

Init Test Dictionary
    @{locationList}    Create List    ${defaultLocation2}    ${defaultLocation1}
    @{rList}    Create List    Auckland Central    Auckland City    West Auckland    Auckland Region    Auckland Airport
    Set Global Variable    @{whereList}    @{locationList}
    Set Global Variable    @{regionList}    @{rList}

    
Default Text Is Available In Search Bar
    [Arguments]    ${defaultValue}
    ${placeholder}    Get Element Attribute    Xpath=//input[@id='searchWhatField' and @name='what']    placeholder
    Log    ${placeholder}
    Should Be Equal    ${placeholder}    ${defaultValue}
    
Default Text Is Available In Location          
    ${placeholder}    Get Element Attribute    Xpath=//input[@id='searchWhereField' and @name='where']    placeholder
    Log    ${placeholder}
    ${return}    Element Should Be Inside The List    ${placeholder}    ${whereList}
    Should Be Equal    ${return}    success
    
Region List Should Be Available When Click The City Name
    [Arguments]    ${region}
    Click Element    id=searchWhereField
    Wait Until Element Is Visible    id=ui-id-2    10
    ${head1}    Get Text    Xpath=//ul[@id='ui-id-2']/li[1]
    Log    ${head1}
    Should Be Equal    ${head1}    Suggestions
    ${li}    Get Text    Xpath=//ul[@id='ui-id-2']/li[2]/div
    ${return}    Element Should Be Inside The List    ${li}    ${region}
    Should Be Equal    ${return}    success
    ${li}    Get Text    Xpath=//ul[@id='ui-id-2']/li[3]/div
    ${return}    Element Should Be Inside The List    ${li}    ${region}
    Should Be Equal    ${return}    success
    
Input A Keyword For Search
    Input Text    id=searchWhatField    hospital
    Wait Until Element Is Visible    id=ui-id-1
    ${head1}    Get Text    Xpath=//ul[@id='ui-id-1']/li[1]
    Should Be Equal    ${head1}    Suggested Categories
    ${li}    Get Text    Xpath=//ul[@id='ui-id-1']/li[2]
    Should Be Equal    ${li}    Hospitals
    Click Button    xpath=//div[@id='searchButton']/button
    Wait Until Element Is Enabled    xpath=//div[@class='search-results listing-fragments']    10
    Capture Page Screenshot
    
Validate Search Result Page Elements
    ${searchkey}    Get Value    id=searchWhatField
    Should Be Equal    ${searchkey}    hospital
    ${nav}    Get Text    xpath=//div[@class='secondary-col']/ol/li[1]/a
    Should Be Equal    ${nav}    Home
    ${nav}    Get Text    xpath=//div[@class='secondary-col']/ol/li[2]/a
    Should Be Equal    ${nav}    Medical & Emergency
    Element Should Be Enabled    css=.view-on-wises-button
    ${hlink}    Get Element Attribute    xpath=//a[@class='view-on-wises-button']    href
    Should Contain    ${hlink}    wises.co.nz/yellow/
    Element Should Be Visible    css=.filters-container
    Click Element    xpath=//div[@class='filters-wrapper']/div[5]/div[1]
    sleep    10
    ${ratingList}    Get Webelements    xpath=//div[@class='filters-wrapper']/div[5]/div[2]/label
    ${number}    Get Length    ${ratingList}
    Should Be Equal As Integers    ${number}    4
    ${blockList}    Get Webelements    css=.listing-wrapper
    ${number}    Get Length    ${blockList}
    ${status}    Evaluate    ${number}>4
    Should Be True    ${status}
    ${buttonText}    Get Text    xpath=//div[@class='primary-col']/section[2]/div[1]/div[1]/div[2]/div[1]/div[1]/a/span
    Should Be Equal    ${buttonText}    Show number
    ${bottomNav}    Get Text    Xpath=//section[@class='pagination']/ul/li[1]/a
    Run Keyword If    ${bottomNav}=='1'    Click Element    css=.icon-chevron-right after-text