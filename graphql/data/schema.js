import { makeExecutableSchema } from 'graphql-tools';
import resolvers from './resolvers';

const typeDefs = `
type Query {
    tokenBySymbol(symbol: String!): Token
    tokenByAddress(address: String!): Token
    allTokens: [Token]
}

type Token {
    address: String!
    symbol: String!
    name: String!
    decimals: Int!
    total_supply: Float!
    transfers: [TokenTransfer]
}

type TokenTransfer {
    id: Int!
    token_address: String!
    from_address: String!
    to_address: String!
    value: Float!
    transaction_hash: String!
    log_index: Int!
    block_number: Int!
    block_hash: String!
}
`;

const schema = makeExecutableSchema({ typeDefs, resolvers });

export default schema;
