const {Telegraf} = require('telegraf');
const bot = new Telegraf('2047079555:AAGAgR6dj1KOqAGSOAo0hBH7BDOSgWtdru0');
const commandsList = require('./commands');

var dutyCommands = require('./duty/duty');

bot.start((ctx) => {
    ctx.replyWithMarkdown('*s-10d3* - бот, созданный для выполнения рутинных классных задач\nНапиши */help*, чтобы узнать подробности...');
});

bot.help((ctx) => {
    let helpText = commandsList.helpText;
    helpText += commandsList.commands.map((command) => `*/${command.command}* - ${command.description}`).join(`\n`);
    ctx.replyWithMarkdown(helpText);
});

bot.command('duty', (ctx) => {
    ctx.replyWithMarkdown(dutyCommands.dutyReply());
});

bot.launch()