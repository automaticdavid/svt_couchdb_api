// view for rpa-account docs
// returns settings sub-jsons


function(doc) {

    var key ;
    var normalized_settings = [] ;


    if (doc.svt_collect_date
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("rpa_account-settings") != -1

        ) {

        // name the properties
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        id = "svt_single" ;
        accountsettings = doc.licenses ;

        count = 1;
        accountsettings.forEach(function(each_setting) {
            var v = {} ;
            v.svt_unic = "setting"+count ;
            v.svt_value = each_setting ;
            normalized_settings.push(v) ;
            count++;
            });



        // map all appliances
        key = [collect, client, source, id]  ;
        emit( key,  {"settings":normalized_settings, "svt_action":"svt_single"} );

    }
}



