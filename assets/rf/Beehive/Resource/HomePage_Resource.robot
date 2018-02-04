*** Settings ***
Resource          Global.robot
Library           NewLibrary
Library           DateTime

*** Variables ***

*** Keywords ***
OpenIndexPage
    Open Browser    ${siteURL}    ${browser}    ${remoteURL}
    print Msg To Some Place    Hello world
    ${str1}    Set Variable    abc
    ${str2}    Set Variable    abc
    ${str3}    Set Variable    abcde
    invokesyskw    ${str1}    ${str2}
    ${output}    invokesyskw2    ${str3}
    ${date}=    Get Current Date
    Log    ${output}
    Log    ${date}

ValidateGroupNumber
    ${lglist}    Get Webelements    Xpath=//div[@id='latestgroups']/div[1]/div    # the list of latest groups
    ${pglist}    Get Webelements    Xpath=//div[@id='populargroups']/div[1]/div    # the list of popular groups
    ${aglist}    Get Webelements    Xpath=//div[@id='allgroups']/div[1]/div    # the list of all groups
    ${lglistnum}    Get Length    ${lglist}
    ${pglistnum}    Get Length    ${pglist}
    ${aglistnum}    Get Length    ${aglist}
    Log    ${lglistnum}
    Log    ${pglistnum}
    Log    ${aglistnum}
    Should Be True    1<=${lglistnum}<=3
    Should Be True    1<=${pglistnum}<=3
    Should Be True    ${aglistnum}>=${lglistnum}
    Should Be True    ${aglistnum}>=${pglistnum}

UserLogIn
    [Arguments]    ${id}    ${pwd}
    Click Element    Xpath=/html/body/div[@id='app']/div/nav[@class='navbar navbar-inverse navbar-fixed-top']/div[@class='container']/div[@class='navbar-collapse collapse']/ul[@class='nav navbar-nav navbar-right']/li/a
    Input Text    css=[type=email]    ${id}
    Input Text    css=[type=password]    ${pwd}
    Click Element    css=.modal-footer>button
