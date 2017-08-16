// view for vipr docs
// returns vdc-storage-pools sub-jsons


function(doc) {

    var key ;

    if (doc.svt_collect_date
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("vipr_vdc-storage-pools_") != -1

        ) {

        // name the fields
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        file =  doc.svt_source_file ;
        elems = file.split("_").slice(2) ;
        id = elems[0] ;




        // map all other
            key = [collect, client, source, id ]  ;
            emit( key, {"storage-pools" : doc, "svt_action":"svt_multi" } );

        }
}