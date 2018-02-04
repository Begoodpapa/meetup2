*** Settings ***
Library           String

*** Keywords ***
RemoveGroup
    [Arguments]    ${gid}
    Click Element    css=#groupRemove
    ${url}=    Set Variable    ${ siteURL}/#/group/manage/remove/${gid}
    Log    ${url}
    Sleep    5    //wait until page content fully loaded
    Click Element    css=#submit_btn
    Sleep    5
    ${message}    Confirm Action    #get the message of Confirmation Window
    Should Contain    ${message}    You will be redirect to the home page
    Choose Ok On Next Confirmation

RetriveGidFromURL
    ${url}    Get Location
    @{urlItemList}    Split String From Right    ${url}    /    2
    Log Many    @{urlItemList}
    ${gid}=    Set Variable    ${urlItemList[1]}
    Log    ${gid}
    [Return]    ${gid}
