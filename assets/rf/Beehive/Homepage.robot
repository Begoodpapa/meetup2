*** Settings ***
Suite Setup       OpenIndexPage
Suite Teardown    Close Browser
Test Setup
Library           Selenium2Library
Resource          Resource/Global.robot
Resource          Resource/HomePage_Resource.robot

*** Test Cases ***
CheckTitleAndNav
    ${PageTitle}    Get Title
    Should Contain    ${PageTitle}    ${IndexPageTitle}
    Page should contain Element    css=.navbar-collapse
    Page Should Contain Link    Persona

CheckPageHeader
    Element should be visible    css=#find
    ${name}    Get Element Attribute    xpath=//header/div[1]@class
    Log    ${name}
    Should Contain Any    ${name}    meetup    find
    sleep    5
    ${name}    Get Element Attribute    xpath=//header/div[1]@class
    Log    ${name}
    Should Contain Any    ${name}    meetup    find
    Page Should Contain    a meetup society
    Page Should Contain    designed for us to find interesting communities and events for sharing and learning.

CheckGroupsInfo
    sleep    15
    Element should be visible    css=.hottest
    Element should be visible    css=.latest
    Element should be visible    css=.all
    sleep    15
    ${lg_number}    Get Matching Xpath Count    xpath=//div[@id='latestgroups']    #amount of div 'latestgroup'. \ It is either 1(group is more than 1) or 0(no any group)
    ${pg_number}    Get Matching Xpath Count    xpath=//div[@id='populargroups']    #amount of div 'populargroup'. \ It is either 1(group is more than 1) or 0(no any group)
    ${ag_number}    Get Matching Xpath Count    xpath=//div[@id='allgroups']    #amount of div 'allgroup'. \ It is either 1(group is more than 1) or 0(no any group)
    Log    ${lg_number}
    Run Keyword If    ${lg_number}==0    Should be equal    ${lg_number} +${pg_number} +${ag_number}    0
    ...    ELSE IF    ${lg_number}>=1    ValidateGroupNumber    #if this is a totally new deployed website.

CheckFooter
    Page Should Contain    designed for us to find interesting communities and events for sharing and learning.
    Element should be visible    css=footer

LoginAndOut
    Click Element    css=.navbar-right>li
    Input Text    css=[type=email]    h3liang
    Input Text    css=[type=password]    8mYY1zD19
    Click Element    css=.modal-footer>button
    Sleep    5
    Page Should Contain    Liang Hui
    Page Should Contain    Log out
    Click Element    css=#basic-nav-dropdown
    Click Element    xpath=//ul[@class='dropdown-menu']/li[5]
    Sleep    2
    Page Should Contain    Log in
