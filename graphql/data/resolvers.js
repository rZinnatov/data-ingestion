import { Token, TokenTransfer } from './connectors';

const resolvers = {
    Query: {
        tokenBySymbol(_, args) {
            return Token.findOne({ where: args });
        },
        tokenByAddress(_, args) {
            args.address = hexToBytes(args.address);
            return Token.findOne({ where: args });
        },
        allTokens() {
            return Token.findAll();
        }
    },
    Token: {
        address(token) {
            return bytesToHex(token.address);
        },
        transfers(token) {
            return TokenTransfer.findAll({
                where: { token_address: token.address }
            });
        }
    },
    TokenTransfer: {
        token_address(tokenTransfer) {
            return bytesToHex(tokenTransfer.token_address);
        },
        from_address(tokenTransfer) {
            return bytesToHex(tokenTransfer.from_address);
        },
        to_address(tokenTransfer) {
            return bytesToHex(tokenTransfer.to_address);
        },
        transaction_hash(tokenTransfer) {
            return bytesToHex(tokenTransfer.transaction_hash);
        },
        block_hash(tokenTransfer) {
            return bytesToHex(tokenTransfer.block_hash);
        }
    }
};

function bytesToHex(hex) {
    return `0x${Buffer.from(hex).toString('hex')}`;
}
function hexToBytes(hex) {
    if (hex.startsWith('0x')) {
        hex = hex.substring(2);
    }

    if (hex.match(/[^0-9a-fA-F]/)) {
        throw new Error('Not a hex string');
    }

    return new Buffer.from(hex, 'hex');
}

export default resolvers;
