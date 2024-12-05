<?php
  $NIOS_baseURL="https://192.168.1.1/wapi/v2.6/";
  $NIOS_User="admin";
  $NIOS_PWD="infoblox";


  #extensibleattributedef

  $ch = curl_init();
  curl_setopt_array($ch,array(
    CURLOPT_USERPWD => $NIOS_User . ":" . $NIOS_PWD,
    CURLOPT_CUSTOMREQUEST => "POST",
    CURLOPT_SSL_VERIFYPEER => false,
#    CURLOPT_VERBOSE => true,
    CURLOPT_TIMEOUT => 30,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_HTTPHEADER => array('Content-Type: application/json')
    )
  );

  $data=[
         [call=>"extensibleattributedef",
         data=>[name=>"R7_Sync", comment=>"R7 Sync the object", type=>"ENUM", flags=>"I", default_value=>"true", list_values=>[[value=>"true"],[value=>"false"]]]],

         [call=>"extensibleattributedef",
         data=>[name=>"R7_SyncedAt", comment=>"R7 Sync Date/Time", type=>"STRING"]],

         [call=>"extensibleattributedef",
         data=>[name=>"R7_NetToSite", comment=>"R7 Add a network to a site", type=>"ENUM", flags=>"I", default_value=>"true", list_values=>[[value=>"true"],[value=>"false"]]]],

         [call=>"extensibleattributedef",
         data=>[name=>"R7_RangeToSite", comment=>"R7 Add a range to a site", type=>"ENUM", flags=>"I", default_value=>"true", list_values=>[[value=>"true"],[value=>"false"]]]],

         [call=>"extensibleattributedef",
         data=>[name=>"R7_ScanOnEvent", comment=>"R7 Scan an asset by an event", type=>"ENUM", flags=>"I", default_value=>"true", list_values=>[[value=>"true"],[value=>"false"]]]],

         [call=>"extensibleattributedef",
         data=>[name=>"R7_ScanOnAdd", comment=>"R7 Scan an asset after provisioning", type=>"ENUM", flags=>"I", default_value=>"true", list_values=>[[value=>"true"],[value=>"false"]]]],

         [call=>"extensibleattributedef",
         data=>[name=>"R7_ScanTemplate", comment=>"R7 Scan template", type=>"ENUM", flags=>"I", default_value=>"default", list_values=>[[value=>"default"],[value=>"full-audit"],[value=>"full-audit-without-web-spider"]]]],

         [call=>"extensibleattributedef",
         data=>[name=>"R7_Site", comment=>"R7 Site name", type=>"ENUM", flags=>"I", default_value=>"Lab", list_values=>[[value=>"Lab"],[value=>"Infoblox"]]]],

         [call=>"extensibleattributedef",
         data=>[name=>"R7_SiteID", comment=>"R7 Site ID. Updated automatically", type=>"INTEGER", default_value=>"0", flags=>"I"]],

         [call=>"extensibleattributedef",
         data=>[name=>"R7_LastScan", comment=>"R7 Last Scan Date. Updated automatically", type=>"STRING", default_value=>"0"]],

         [call=>"extensibleattributedef",
         data=>[name=>"R7_AddByHostname", comment=>"R7 Add a host by a hostname", type=>"ENUM", flags=>"I", default_value=>"true", list_values=>[[value=>"true"],[value=>"false"]]]],


  ];

  foreach ($data as $api_call){
    $data_string = json_encode($api_call{data});
    curl_setopt($ch, CURLOPT_URL, $NIOS_baseURL.$api_call{call});
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data_string);

    $result = curl_exec($ch);
  #  print_r($result);
    $httpcode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $res=json_decode($result);
    print_r($res);
  };

  curl_close($ch);

?>
