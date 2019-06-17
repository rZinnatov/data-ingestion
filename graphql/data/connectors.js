import Sequelize from 'sequelize';

const db = new Sequelize('postgresql://terminal_user:terminal_pass@localhost:5432/terminal');

const TokenModel = db.define('token', {
    address: { type: Sequelize.STRING, primaryKey: true },
    symbol: { type: Sequelize.STRING },
    name: { type: Sequelize.STRING },
    decimals: { type: Sequelize.INTEGER },
    total_supply: { type: Sequelize.FLOAT },
}, {
    tableName: 'token',
    timestamps: false,
    underscored: true,
    freezeTableName: true,
});

const TokenTransferModel = db.define('tokenTransfer', {
    id: { type: Sequelize.INTEGER, primaryKey: true },
    token_address: { type: Sequelize.STRING },
    from_address: { type: Sequelize.STRING },
    to_address: { type: Sequelize.STRING },
    value: { type: Sequelize.FLOAT },
    transaction_hash: { type: Sequelize.STRING },
    log_index: { type: Sequelize.INTEGER },
    block_number: { type: Sequelize.INTEGER },
    block_hash: { type: Sequelize.STRING },
}, {
    tableName: 'token_transfer',
    timestamps: false,
    underscored: true,
    freezeTableName: true,
});

TokenModel.hasMany(TokenTransferModel);
TokenTransferModel.belongsTo(TokenModel);

const Token = db.models.token;
const TokenTransfer = db.models.tokenTransfer;

export { Token, TokenTransfer };
