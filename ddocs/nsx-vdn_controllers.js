// view for nsx-vdn docs
// returns controller sub-jsons



function(doc) {

    var key ;
    var normalized_controllers = [] ;

    if (doc.svt_collect_date
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("nsx_vdn-controller") != -1
            && doc.controllers
            //&& doc.id

        ) {

        // name the fields
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        id = "svt_single";
        controllers = doc.controllers ;

        // loop the features & find the correct one
        var counter = 1;
        controllers.forEach(function(controller) {
            var v = {} ;
            v.svt_unic = "controller"+counter ;
            v.svt_value = controller ;
            normalized_controllers.push(v) ;
            counter++;
        }) ;


        // map all controllers
        key = [collect, client, source, id]  ;
        emit( key,  {"controllers":normalized_controllers, "svt_action":"svt_single"} );

    }
}
