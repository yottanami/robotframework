*** Settings ***
Suite Setup      Run Tests    -L DEBUG    standard_libraries/process/secrets.robot
Resource         atest_resource.robot

*** Test Cases ***
Run Process with Secret Argument
    Python script should be run and arguments logged    <secret>

Run Process with Mixed Arguments Including Secret
    Python script should be run and arguments logged    public_arg <secret>

Run Process with Stdin as Secret
    Check Test Case    ${TESTNAME}

Start Process with Secret Argument
    Python script should be run and arguments logged    <secret>

Start Process with Stdin as Secret
    Check Test Case    ${TESTNAME}

Secret in environment variable via env Dict
    ${tc} =    Check Test Case    ${TESTNAME}
    Check Log Message    ${tc[1, 1]}    *env:*'v1': '<secret>'*    level=DEBUG    pattern=yes
    Secret should not be logged    ${tc[1, 1]}

Secret in environment variable via env:name Syntax
    ${tc} =    Check Test Case    ${TESTNAME}
    Check Log Message    ${tc[0, 1]}    *env:*'v2': '<secret>'*    level=DEBUG    pattern=yes
    Secret should not be logged    ${tc[0, 1]}

Multiple Secrets in environment variables
    ${tc} =    Check Test Case    ${TESTNAME}
    Check Log Message    ${tc[0, 1]}    *env:*'v1': '<secret>'*    level=DEBUG    pattern=yes
    Check Log Message    ${tc[0, 1]}    *env:*'v3': '<secret>'*    level=DEBUG    pattern=yes
    Secret should not be logged    ${tc[0, 1]}

*** Keywords ***
Python script should be run and arguments logged
    [Arguments]    ${arguments}    ${script}=script.py    ${index}=0
    ${script} =    Normalize Path    ${DATADIR}/standard_libraries/process/files/${script}
    ${tc} =    Arguments should be logged    python ${script} ${arguments}    ${index}
    RETURN    ${tc}

Secret should not be logged
    [Arguments]    ${msg}
    Should Not Contain    ${msg.message}    This is secret!

Arguments should be logged
    [Arguments]    ${message}    ${index}=0
    ${tc} =    Check Test Case    ${TESTNAME}
    Check Log Message    ${tc[${index}, 0]}    Starting process:\n${message}
    RETURN    ${tc}
