// view for vro misc docs
// returns actions sub-jsons


function(doc) {

    var key ;
    var normalized_actions = [] ;

    if (doc.svt_collect_date
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("vro_actions") != -1

        ) {

        // name the properties
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        id = "svt_single" ;
        actions = doc.link ;

        count = 1;
        actions.forEach(function(action) {
            var v = {} ;
            v.svt_unic = "action"+count ;
            v.svt_value = action ;
            normalized_actions.push(v) ;
            count++;
            }
        ) ;

        // map all appliances
        key = [collect, client, source, id]  ;
        emit( key,  {"actions":normalized_actions, "svt_action":"svt_single"} );

    }
}

