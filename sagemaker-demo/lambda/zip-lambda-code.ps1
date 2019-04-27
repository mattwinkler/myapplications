param( 
  [string]$functionname,
  [string]$version
 )

$configFilePath = $PSScriptRoot
$source = "$configFilePath\$functionname\*"
$destination = "$configFilePath\$functionname\$functionname-$version.zip"

If(Test-path $destination) {Remove-item $destination}
Compress-Archive -Path $source -DestinationPath $destination