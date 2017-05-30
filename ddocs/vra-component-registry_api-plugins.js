// view for vra-component-registry docs
// returns api-plugins sub-jsons



function(doc) {

    var key ;
    var normalized_plugins = [] ;

    if (doc.svt_collect_date
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("vra_component-registry-api-plugins.json") != -1



        ) {

        // name the fields
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        id = "svt_single";
        plugins = doc.content ;

        // loop the features & find the correct one
        var count = 1;
        plugins.forEach(function(each_plugin) {
            var v = {} ;
            v.svt_unic = "plugin"+count ;
            v.svt_value = each_plugin ;
            normalized_plugins.push(v) ;
            count ++;
        }) ;


        // map all controllers
        key = [collect, client, source, id]  ;
        emit( key,  {"api-plugins":normalized_plugins, "svt_action":"svt_single"} );

    }
}
