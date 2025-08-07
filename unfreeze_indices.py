from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError, TransportError
import argparse

def unfreeze_all_indices(es_client):
    try:
        # Get all frozen indices (indices with the 'frozen' attribute)
        frozen_indices = es_client.cat.indices(index='*', h='index,settings.index.frozen', format='json')
        
        indices_to_unfreeze = []
        for idx in frozen_indices:
            if idx.get('settings.index.frozen') == 'true':
                indices_to_unfreeze.append(idx['index'])
        
        if not indices_to_unfreeze:
            print("No frozen indices found in the cluster.")
            return
        
        print(f"Found {len(indices_to_unfreeze)} frozen indices:")
        for idx in indices_to_unfreeze:
            print(f" - {idx}")
        
        # Unfreeze each index
        success_count = 0
        for index_name in indices_to_unfreeze:
            try:
                es_client.index.open(index=index_name)
                print(f"Successfully unfroze index: {index_name}")
                success_count += 1
            except Exception as e:
                print(f"Failed to unfreeze index {index_name}: {str(e)}")
        
        print(f"\nOperation complete. Successfully unfroze {success_count}/{len(indices_to_unfreeze)} indices.")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Unfreeze all frozen indices in Elasticsearch 7.17')
    parser.add_argument('--host', default='http://localhost:9200', help='Elasticsearch host URL')
    parser.add_argument('--username', help='Elasticsearch username')
    parser.add_argument('--password', help='Elasticsearch password')
    parser.add_argument('--verify-certs', action='store_true', help='Verify SSL certificates')
    
    args = parser.parse_args()
    
    # Configure Elasticsearch client
    es_config = {
        'hosts': [args.host],
        'verify_certs': args.verify_certs
    }
    
    if args.username and args.password:
        es_config['http_auth'] = (args.username, args.password)
    
    try:
        es = Elasticsearch(**es_config)
        if not es.ping():
            raise Exception("Could not connect to Elasticsearch cluster")
        
        cluster_info = es.info()
        print(f"Connected to Elasticsearch cluster: {cluster_info['cluster_name']} (Version: {cluster_info['version']['number']})")
        
        if not cluster_info['version']['number'].startswith('7.17.'):
            print("Warning: This script is designed for Elasticsearch 7.17.x but you're running a different version.")
        
        unfreeze_all_indices(es)
    
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()