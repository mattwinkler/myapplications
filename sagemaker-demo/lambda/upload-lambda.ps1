param( 
  [string]$bucket,
  [string]$functionname,
  [string]$version
 )

$configFilePath = $PSScriptRoot
$source = "$configFilePath\$functionname\$functionname-$version.zip"
     
aws s3 cp $source s3://$bucket/code/ --profile default