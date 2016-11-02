// view for nsx-appliance docs
// returns locale sub-jsons


function(doc) {

    var key ;

    if (doc.svt_collect_date
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("nsx_appliance-management-system-locale") != -1


        ) {

        // name the properties
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        id = "svt_group" ;

        // map all appliances
        key = [collect, client, source, id]  ;

        emit( key,  {"locale":doc} );

    }
}
