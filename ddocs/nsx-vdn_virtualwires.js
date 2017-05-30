// view for nsx-vdn docs
// returns virtualswires sub-jsons



function(doc) {

    var key ;
    var normalized_vwires = [] ;

    if (doc.svt_collect_date
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("nsx_vdn-virtualwires") != -1
            //&& doc.id

        ) {

        // name the fields
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        id = "svt_single";
        vwires = doc.dataPage.data ;

        // loop the features & find the correct one
        var count = 1;
        vwires.forEach(function(vwire) {
            var v = {} ;
            v.svt_unic = "vwire"+count ;
            v.svt_value = vwire ;
            normalized_vwires.push(v) ;
            count ++;
        }) ;


        // map all controllers
        key = [collect, client, source, id]  ;
        emit( key,  {"virtualwires":normalized_vwires, "svt_action":"svt_single"} );

    }
}
