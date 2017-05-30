// view for vra-catalog-service docs
// returns services sub-jsons



function(doc) {

    var key ;
    var normalized_services = [] ;

    if (doc.svt_collect_date
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("vra_catalog-service-services.json") != -1



        ) {

        // name the fields
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        id = "svt_single";
        services = doc.content ;

        // loop the features & find the correct one
        var count = 1;
        services.forEach(function(each_service) {
            var v = {} ;
            v.svt_unic = "service"+count ;
            v.svt_value = each_service ;
            normalized_services.push(v) ;
            count ++;
        }) ;


        // map all controllers
        key = [collect, client, source, id]  ;
        emit( key,  {"services":normalized_services, "svt_action":"svt_single"} );

    }
}
