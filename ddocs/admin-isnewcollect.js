function(doc) {

    if (doc.svt_collect_date 
         && doc.svt_client
        ) {
        
        // name the fields    
        collect = doc.svt_collect_date ;
        client = doc.svt_client ;
            
        emit([collect, client], 1) ;
        
    }
}
