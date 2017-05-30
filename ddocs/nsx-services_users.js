// view for nsx-services docs
// returns users sub-jsons



function(doc) {

    var key ;
    var normalized_users = [] ;

    if (doc.svt_collect_date
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("nsx_services-usermgmt-users-vsm.json") != -1

        ) {

        // name the fields
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        id = "svt_single";
        users = doc.users ;

        // loop the features & find the correct one
        var count = 1;
        users.forEach(function(user) {
            var v = {} ;
            v.svt_unic = "users"+count ;
            v.svt_value = user ;
            normalized_users.push(v) ;
            count++;
        }) ;


        // map all controllers
        key = [collect, client, source, id]  ;
        emit( key,  {"users":normalized_users, "svt_action":"svt_single"} );

    }
}
