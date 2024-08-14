Param(
    $Username,
    $Password
)
$SecuredPassword = ConvertTo-SecureString $Password -AsPlainText -Force

New-LocalUser -Name $Username -Password $SecuredPassword
