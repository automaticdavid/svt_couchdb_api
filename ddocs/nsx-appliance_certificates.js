// view for nsx-appliance docs
// returns certificates sub-jsons


function(doc) {

    var key ;
    var normalized_certificates = [] ;

    if (doc.svt_collect_date
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("nsx_appliance-management-certificatemanager-certificates-nsx") != -1

        ) {

        // name the properties
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        id = "svt_single" ;
        certificates = doc.certificates ;

        // loop the plugins
        var counter=1;
       certificates.forEach(function(certificate) {
            var v = {} ;
            if (certificate) {
                v.svt_unic = "certificate"+counter;
                v.svt_value = certificate ;
                normalized_certificates.push(v) ;
                counter++;
            }
        }) ;

        // map all appliances
        key = [collect, client, source, id]  ;
        emit( key,  {"certificates":normalized_certificates, "svt_action":"svt_single"} );

    }
}
