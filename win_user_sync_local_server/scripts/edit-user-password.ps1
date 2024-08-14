# User name
Param(
    $Username,
    $Password
)
$SecuredPassword = ConvertTo-SecureString $Password -AsPlainText -Force

$UserAccount = Get-LocalUser -Name $Username
$UserAccount | Set-LocalUser -Password $SecuredPassword
