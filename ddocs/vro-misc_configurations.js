// view for vro misc docs
// returns configurations sub-jsons


function(doc) {

    var key ;
    normalized_configurations = [];


    if (doc.svt_collect_date
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("vro_configurations") != -1

        ) {

        // name the properties
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        id = "svt_single" ;
        configurations = doc.link ;

        count = 1;
        configurations.forEach(function(configuration) {
            var v = {} ;
            v.svt_unic = "configuration"+count ;
            v.svt_value = configuration ;
            normalized_configurations.push(v) ;
            count++;
            }
        );

        // map all appliances
        key = [collect, client, source, id]  ;
        emit( key,  {"configurations":normalized_configurations, "svt_action":"svt_single"} );

    }
}


