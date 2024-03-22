# Deduction, Deduce

## Category
Forensics

## Estimated difficulty
Easy

## Description
Parsing XML data into a queryable format, understanding Scheduled Tasks properties, deduction by elemination

## Scenario
A woman is sure she was hacked but our officers made a huge mistake when acquiring the evidences and most of it has been lost! Only two configuration files and an extract of the Scheduled Tasks remains along with a copy of the interview conducted with the victim. Can you make the correct assumptions and deduce which Scheduled Task is most likely responsible for the ongoing madness?

## Write-up
There are 4 pieces of information
- config.properties appears to be a config file of some sorts which references some color coding for text
- Interview.pdf is the primary source of information to deduct which Scheduled Task has the correct Flag
- Microsoft.PowerShell_profile.ps1 is a PowerShell profile which references color coding for text
- ScheduledTasks.xml is a long list of multiple Scheduled Tasks in the xml format

The `config.properties` doesn't reveal a lot of additional information aside from what can be directly observed. The `PowerShell_profile` file appears to be very similar but contains some strange values. By [googling]("https://en.wikipedia.org/wiki/ANSI_escape_code#Colors_") the ```e[41;30m`` sequence can be interpreted as "Black foreground, Red background". 

Reviewing the `Interview.pdf` multiple items could be hints towards the scheduled task:

- `hideous green screen appeared`
- `Some red letters`
- `numbers were in black and had a red-ish background` 

These three items already appear very closely linked to what was observed in the `config` & `PowerShell` file. The key difference is that in the `config` file we only know that "Number" is set to red. The `PowerShell` clearly indicates the number foreground is black and the background is red. Most likely the correct flag will be linked to a PowerShell based Scheduled Task.

Looking further at the interview there are some other hints.

- `November 9th 2023 at 10 AM`
- `she uses the laptop every Tuesday while I take it with me on Thursdays`

The first item could point towards a potential creation date for the Scheduled Task. The second entry provides further information on potential timeframes; at a minimum the laptop is used every Tuesday & Thursday. Looking at the calendar November 9th was a Thursday. Assuming the 9th was indeed the first appearance of the strange screens the Scheduled Task was most likely created between November 7th end of business day and November 8th approximately 10 AM.

- `she (Elisa) never noticed it`
- `forgot the charger`

A specific mention of one person never experiencing the strange screens whereas other users have seen them. This specific user only used the laptop once however and the laptop was not connected to the power grid (therefore using battery power).

- `eli.dun`
- `eli.set`
- `est.bir`

References to the respective accounts.

The ScheduledTasks.xml file contains many different scheduled tasks, so we need to find the correct one. Let's take a random scheduled tasks to see what kind of information is available:

```
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2"
    xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
    <RegistrationInfo>
        **<Date>2023-11-14T9:7:52:1191852</Date>**
        <Author>Sora</Author>
        **<URI>CSC{The_Gr&lt;wtes!_Degective_4m_live}</URI>**
    </RegistrationInfo>
    <Principals>
        <Principal id="Author">
            <UserId>S-1-5-21-1308737159-2471153319-3326108015-1001</UserId>
            <LogonType>InteractiveToken</LogonType>
            <RunLevel>LeastPrivilege</RunLevel>
        </Principal>
    </Principals>
    <Settings>
        <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
        **<DisallowStartIfOnBatteries>FALSE</DisallowStartIfOnBatteries>
        <StopIfGoingOnBatteries>FALSE</StopIfGoingOnBatteries>**
        <AllowHardTerminate>true</AllowHardTerminate>
        <StartWhenAvailable>false</StartWhenAvailable>
        <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
        <IdleSettings>
            <StopOnIdleEnd>true</StopOnIdleEnd>
            <RestartOnIdle>false</RestartOnIdle>
        </IdleSettings>
        <AllowStartOnDemand>true</AllowStartOnDemand>
        **<Enabled>true</Enabled>**
        <Hidden>true</Hidden>
        <RunOnlyIfIdle>false</RunOnlyIfIdle>
        <WakeToRun>false</WakeToRun>
        <ExecutionTimeLimit>PT72H</ExecutionTimeLimit>
        <Priority>7</Priority>
    </Settings>
    <Actions Context="Author">
        <Exec>
            **<Command>Powershell.exe</Command>**
            **<Arguments>C:\User\eli.set\Downloads\zero.exe</Arguments>**
        </Exec>
    </Actions>
    <Triggers xmlns="">
        **<LogonTrigger>
            <Enabled>True</Enabled>
        </LogonTrigger>**
    </Triggers>
</Task><?xml version="1.0" encoding="UTF-16"?>
```

The `URI` property seems to contain something resembling a flag (there are over 1000 in the file), there's a `Date` property indicating when the Task was created, there are two entries regarding battery usage `DisallowStartIfOnBatteries` and `StopIfGoingOnBatteries`, the `Enabled` entry highlights if the Scheduled Task is active or not, there are two properties linked to program execution `Command` and `Arguments` and lastly there's the `LogonTrigger`. The presence of this last node in the XML would indicate that the scheduled task is triggered as soon as someone logs in. If all tasks have this same trigger a combination of this trigger with a `DisallowStartIfOnBatteries` set to `TRUE` would explain why Elisa never saw the weird screens.

Putting all the information together we would need to parse the different Scheduled Task entries and search for a Scheduled Task that fullfills the following requirements:

- `DisallowStartIfOnBatteries` set to `TRUE`
- `Enabled` set to `TRUE`
- `Command` contains `Powershell`
- `Date` set between November 7th end of business day and November 8th approximately 10 AM

Using these filters a single entry appears

|Flag|Command|Arguments|Date|DisallowStartIfOnBatteries|Enabled|
|CSC{The_$reytsst_Dete35ive_Ty_l0v3}|Powershell.exe|echo 1>update.txt; transparent.exe|2023-11-09T7:23:54:4408106|True|True|

## Solve script
null

## Flag
CSC{The_$reytsst_Dete35ive_Ty_l0v3}

## Creator
Sora

## Creator bio
I am but a line in a contract
