*** Settings ***
Documentation     This is a practice for Robot Framework
Suite Setup       OpenIndexPage
Library           SeleniumLibrary
Resource          Resource/Global.robot
Resource          Resource/HomePage_Resource.robot
Resource          Resource/Group_Resource.robot
Resource          ../aa/Group_Resource.robot

*** Variables ***

*** Test Cases ***
CreateGroupNormalDefaultImg
    [Documentation]    As a user I can open the home page and see the head and body information
    [Tags]    PracticeTag
    Click Element    Xpath=/html/body/div[@id='app']/div/nav[@class='navbar navbar-inverse navbar-fixed-top']/div[@class='container']/div[@class='navbar-collapse collapse']/ul[@class='nav navbar-nav']/li[1]/a
    ${logintext}    Get Text    Xpath=/html/body/div[@id='app']/div/nav[@class='navbar navbar-inverse navbar-fixed-top']/div[@class='container']/div[@class='navbar-collapse collapse']/ul[@class='nav navbar-nav navbar-right']/li/a    #check whether the page has the text 'Log in', which mean the user has not signed in beforehand
    Log    ${logintext}
    Run Keyword if    '${logintext}'=='Log in'    UserLogIn    h3liang    8mYY1zD19    #sometimes user is not signed in
    ${groupname}    Catenate    TestGroup    _    ${browser}
    ${groupdesc}    Set Variable    This is the description of a test group
    Input Text    css=#inputName    ${groupname}
    Input Text    css=.simditor-body    ${groupdesc}
    Wait Until Element Is Visible    css=#submit_btn    5
    Click Element    css=#submit_btn
    Sleep    5
    ${message}    Confirm Action    #get the message of Confirmation Window
    Should Contain    ${message}    Do you want to redirect to the home page of this group?
    Choose Ok On Next Confirmation
    Sleep    5
    Element Text Should Be    css=#head_group_name    TestGroup _ chrome
    ${groupid}    RetriveGidFromURL
    RemoveGroup    ${groupid}
    [Teardown]

CreateGroupNormalCustomImg
    [Tags]    2
    Click Element    Xpath=/html/body/div[@id='app']/div/nav[@class='navbar navbar-inverse navbar-fixed-top']/div[@class='container']/div[@class='navbar-collapse collapse']/ul[@class='nav navbar-nav']/li[1]/a
    ${logintext}    Get Text    Xpath=/html/body/div[@id='app']/div/nav[@class='navbar navbar-inverse navbar-fixed-top']/div[@class='container']/div[@class='navbar-collapse collapse']/ul[@class='nav navbar-nav navbar-right']/li/a    #check whether the page has the text 'Log in', which mean the user has not signed in beforehand
    Log    ${logintext}
    Log    ${CURDIR}
    Run Keyword if    '${logintext}'=='Log in'    UserLogIn    h3liang    8mYY1zD19    #sometimes user is not signed in
    ${groupname}    Catenate    TestGroup    _    ${browser}
    ${groupdesc}    Set Variable    This is the description of a test group
    Input Text    css=#inputName    ${groupname}
    Input Text    css=.simditor-body    ${groupdesc}
    Choose File    css=#selectedFile    ${CustomIMGSrc}
    Click Element    Xpath=/html/body/div[@id='app']/div/div[@class='row']/div[@class='col-md-10 col-md-offset-1']/div[@class='panel panel-default']/div[@class='panel-className']/form[@id='GroupForm1']/div[5]/div[2]/div[@class='box']/input
    Wait Until Element Is Visible    css=#submit_btn    5
    Click Element    css=#submit_btn
    Sleep    5
    ${message}    Confirm Action    #get the message of Confirmation Window
    Should Contain    ${message}    Do you want to redirect to the home page of this group?
    Choose Ok On Next Confirmation
    Sleep    5
    Element Text Should Be    css=#head_group_name    TestGroup _ chrome
    Element Text should Be    css=#groupdesc    ${groupdesc}
    ${ImgSrc}    Get Element Attribute    css=#groupCarousel>div>div>img@src
    Log    ${ImgSrc}
    #Should Contain    ${ImgSrc}    ${imgname}
    ${groupid}    RetriveGidFromURL
    RemoveGroup    ${groupid}

*** Keywords ***