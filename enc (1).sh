for bucket_name in $(aws s3api list-buckets --query "Buckets[].Name" --output text); do

    echo ${bucket_name}
    
    encryption_info=$(aws s3api get-bucket-encryption \
        --bucket ${bucket_name} 2>/dev/null)
        
    if [[ $? != 0 ]]; then
        echo " - no-encryption"
    else
        echo " - ${encryption_info}"
    fi
done

# Check EBS volumes for encryption.
aws ec2 describe-volumes --filters Name=encrypted,Values=false | jq '.Volumes[] | .VolumeId ,.Encrypted'

# Get encryption info of all the snapshots owned by user.
for snapshot in $(aws ec2 describe-snapshots --region us-east-1 \
--owner-ids $(aws sts get-caller-identity --query "Account" --output text) \
--filters Name=status,Values=completed --output table --query 'Snapshots[*].SnapshotId' \
--output text); do aws ec2 describe-snapshots --region us-east-1 --snapshot-id $snapshot --query 'Snapshots[*].Encrypted';done