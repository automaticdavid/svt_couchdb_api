// view for nsx-vdn docs
// returns scopes sub-jsons



function(doc) {

    var key ;
    var normalized_scopes = [] ;

    if (doc.svt_collect_date
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("nsx_vdn-scopes") != -1
            && doc.allScopes
            //&& doc.id

        ) {

        // name the fields
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        id = "svt_single";
        scopes = doc.allScopes ;

        // loop the features & find the correct one
        var counter = 1;
        scopes.forEach(function(scope) {
            var v = {} ;
            v.svt_unic = "scopes"+counter ;
            v.svt_value = scope ;
            normalized_scopes.push(v) ;
            counter++;
        }) ;


        // map all controllers
        key = [collect, client, source, id]  ;
        emit( key,  {"scopes":normalized_scopes, "svt_action":"svt_single"} );

    }
}
