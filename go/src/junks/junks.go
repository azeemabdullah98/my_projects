package main

import (
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/dynamodb"
	"github.com/aws/aws-sdk-go/service/dynamodb/dynamodbattribute"
)

var dynamo *dynamodb.DynamoDB

// connectDynamo returns a dynamoDB client
func connectDynamo() (db *dynamodb.DynamoDB) {
	return dynamodb.New(session.Must(session.NewSession(&aws.Config{
		Region: &us-east-2,
	})))
}
func (c *DynamoDB) Query(input *QueryInput) (*QueryOutput, error) {
	result,err := dynamo.query(&dynamodb.QueryInput{
		Key : map[string]*dynamodb.AttributeValue{
			"Type":{
				'S':aws.String("dry"),
			},
		},
		TableName: &price_comparison
	})
	if err != nil {
		return StdClass3,err
	}
	err = dynamodb.UnmarshalMap(result.Item, &StdClass3)
	return StdClass3,err
}