import argparse
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError, TransportError
import sys
import re

def validate_index_name(index_name):
    """Validate index name format (e.g., fg-009783)."""
    pattern = r'^[A-Za-z]+-\d{6}$'
    return bool(re.match(pattern, index_name))

def parse_index_range(start_index, end_index):
    """Parse index range and return list of index names."""
    try:
        start_num = int(start_index.split('-')[-1])
        end_num = int(end_index.split('-')[-1])
        if start_num > end_num:
            raise ValueError("Start index number must be less than or equal to end index number.")
        prefix = start_index[:start_index.rfind('-')]
        return [f"{prefix}-{str(i).zfill(6)}" for i in range(start_num, end_num + 1)]
    except ValueError as e:
        raise ValueError(f"Invalid index format: {str(e)}")

def reindex(es_client, source_index, dest_index, alias=None):
    """Reindex a single index and optionally assign an alias."""
    try:
        # Check if source index exists
        if not es_client.indices.exists(index=source_index):
            print(f"Source index {source_index} does not exist. Skipping.")
            return False

        # Create destination index if it doesn't exist
        if not es_client.indices.exists(index=dest_index):
            es_client.indices.create(index=dest_index)

        # Add alias to the reindexed index if specified
        if alias:
            try:
                es_client.indices.put_alias(index=dest_index, name=alias)
                print(f"Added alias {alias} to {dest_index}")
            except Exception as e:
                print(f"Error adding alias {alias} to {dest_index}: {str(e)}")
        
            # Set index.lifecycle.indexing_complete to true
            try:
                es_client.indices.put_settings(
                    index=dest_index,
                    body={
                        "settings": {
                            "index.lifecycle.indexing_complete": True
                        }
                    }
                )
                print(f"Set index.lifecycle.indexing_complete=true for {dest_index}")
            except Exception as e:
                print(f"Warning: Could not set indexing_complete for {dest_index}: {e}")
                
        # Perform reindex
        response = es_client.reindex(
            body={
                "source": {"index": source_index},
                "dest": {"index": dest_index}
            },
            wait_for_completion=True
        )
        print(f"Reindexed {source_index} to {dest_index}: {response['took']}ms, "
              f"Created: {response['created']}, Updated: {response['updated']}")

        return True
    except Exception as e:
        print(f"Error reindexing {source_index} to {dest_index}: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Reindex Elasticsearch indexes.")
    parser.add_argument('--host', default='localhost:9200', help='Elasticsearch host (default: localhost:9200)')
    parser.add_argument('--username', help='Elasticsearch username')
    parser.add_argument('--password', help='Elasticsearch password')
    parser.add_argument('--start-index', required=True, help='Start index name (e.g., fg-009783)')
    parser.add_argument('--end-index', required=True, help='End index name (e.g., fg-009789)')
    parser.add_argument('--alias', help='Alias to assign to reindexed indexes')
    parser.add_argument('--verify-certs', action='store_false', help='Verify SSL certificates')
    
    args = parser.parse_args()

    # Validate index names
    if not (validate_index_name(args.start_index) and validate_index_name(args.end_index)):
        print("Index names must be in format 'adc-######' (e.g., fg-009783)")
        sys.exit(1)

    # Initialize Elasticsearch client
    try:
        es_client = Elasticsearch(
            [args.host],
            basic_auth=(args.username, args.password) if args.username and args.password else None,
            verify_certs: args.verify_certs
        )
    except Exception as e:
        print(f"Failed to connect to Elasticsearch: {str(e)}")
        sys.exit(1)

    # Get list of indexes to reindex
    try:
        indexes = parse_index_range(args.start_index, args.end_index)
    except ValueError as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

    # Reindex each index
    for source_index in indexes:
        dest_index = f"{source_index}-reindexed"
        print(f"Starting reindex from {source_index} to {dest_index}")
        success = reindex(es_client, source_index, dest_index, args.alias)
        if success:
            print(f"Successfully reindexed {source_index}")
        else:
            print(f"Failed to reindex {source_index}")

if __name__ == "__main__":
    main()