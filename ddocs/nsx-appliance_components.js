// view for nsx_appliance docs
// returns components sub-jsons

function(doc) {

    var key ;
    var normalized_components = [] ;

    if (doc.svt_collect_date
        && doc.svt_client
        && doc.svt_source
        && doc.svt_source_file
        && doc.svt_source_file.indexOf("nsx_appliance-management-components") != -1
        && doc.components
        ) {

        // name the fields
    collect = doc.svt_collect_date ;
    client = doc.svt_client ;
    source = doc.svt_source ;
    id = "svt_single";
    components = doc.components ;

        // loop the features & find the correct one
        components.forEach(function(component) {
            var v = {} ;
            if (component.componentId) {
               v.svt_unic = component.componentId ;
               v.svt_value = component ;
               normalized_components.push(v) ;
           }
       }) ;

        // map all controllers
        key = [collect, client, source, id]  ;
        emit( key,  {"components":normalized_components, 'svt_action':'svt_single'} );

    }
}
