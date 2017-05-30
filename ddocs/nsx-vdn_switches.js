// view for nsx-vdn docs
// returns switches sub-jsons



function(doc) {

    var key ;
    var normalized_switches = [] ;

    if (doc.svt_collect_date
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("nsx_vdn-switches") != -1
            && doc.switches
            //&& doc.id

        ) {

        // name the fields
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        id = "svt_single";
        switches = doc.switches ;

        // loop the features & find the correct one
        var count = 1;
        switches.forEach(function(each_switch) {
            var v = {} ;
            v.svt_unic = "switch"+count ;
            v.svt_value = each_switch ;
            normalized_switches.push(v) ;
            count ++;
        }) ;


        // map all controllers
        key = [collect, client, source, id]  ;
        emit( key,  {"switches":normalized_switches, "svt_action":"svt_single"} );

    }
}
