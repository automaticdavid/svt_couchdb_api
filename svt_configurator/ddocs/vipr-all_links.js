// view for vipr_ docs
// returns all docs but with the vipr URN as key

function(doc) {
    
    var key ; 
    var links = {} ;
    
    if (doc.svt_collect_date 
            && doc.svt_client
            && doc.svt_source
            && doc.svt_source_file
            && doc.svt_source_file.indexOf("vipr_") != -1
            && doc.id
        
        ) {
        
        // name the fields
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
        source = doc.svt_source ;
        svt_urn = doc.id ;
        
        // map with the urn as key for values
        links[svt_urn] = doc ;
        key = [collect, client, source]  ;
        emit( key,  links );
        
    }
}