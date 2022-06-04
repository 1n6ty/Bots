require('dotenv').config()

import { Client, GuildMember, Intents, VoiceChannel } from "discord.js";

const client = new Client({ intents: [
  Intents.FLAGS.GUILDS,
  Intents.FLAGS.GUILD_MESSAGES,
  Intents.FLAGS.GUILD_VOICE_STATES,
  Intents.FLAGS.GUILD_MEMBERS
] });

let headMasters = new Map<GuildMember | null, VoiceChannel>();

function getKeyByChannel(id: string): GuildMember | null{
  for(let [key, v] of headMasters.entries()){
    if(v.id == id) return key;
  }
  return null;
}

client.on('ready', async () => {
  client.application?.commands.create({
    name: 'user-limit',
    description: 'Set user limit',
    default_permission: false,
    options: [
      {
        type: 4,
        name: 'limit',
        description: 'user limit',
        required: true
      }
    ]
  }, "668497756691759124");
  client.application?.commands.create({
    name: 'disconnect',
    description: 'Disconnect user',
    default_permission: false,
    options: [
      {
        type: 6,
        name: 'user',
        description: 'user to disconnect',
        required: true
      }
    ]
  }, "668497756691759124");

  console.log(`The_Head was logged as ${client.user?.tag}`);
});

client.on('voiceStateUpdate', async (oldState, newState) => {
  if(oldState.channel && newState.channelId != oldState.channelId && headMasters.get(oldState.member) && headMasters.get(oldState.member)!.id == oldState.channel.id){
    let voiceRule = await oldState.guild.roles.fetch("981830785940205679");
    oldState.member?.roles.remove(voiceRule!);
    if(oldState.channel.members.size > 0){
      headMasters.set(oldState.channel.members.at(0)!, headMasters.get(oldState.member)!);
      oldState.channel.members.at(0)!.roles.add(voiceRule!);
      headMasters.delete(oldState.member);
    } else{
      await headMasters.get(oldState.member)!.delete();
      headMasters.delete(oldState.member);
    }
  }
  if(newState.channel){
    if(newState.channel.name == "✨{₺01n2m∆k3!n3w!4∆nn3l}°"){
      let newVoiceChannel = await newState.guild.channels.create(`🔊 V0ic3`, {
        type: "GUILD_VOICE",
        parent: newState.channel.parentId!
      });
      await newState.member?.voice.setChannel(newVoiceChannel);
      headMasters.set(newState.member, newVoiceChannel);
      let voiceRule = await newState.guild.roles.fetch("981830785940205679");
      newState.member?.roles.add(voiceRule!);
    }
  }
});

client.on('interactionCreate', async interaction => {
  if(!interaction.isCommand()) return;

  if(interaction.command?.name == 'user-limit'){
    let limit = interaction.options.getInteger('limit');
    let user = getKeyByChannel(interaction.channel?.id!);
    let obj = headMasters.get(user);
    if(limit && limit > 0 && user && user.id == interaction.user.id){
      obj?.setUserLimit(limit);
      interaction.reply({content: `User limit has been set to ${limit}!`});
    }
  }
  if(interaction.command?.name == 'disconnect'){
    let userToD = interaction.options.getUser('user');
    let obj = headMasters.get(getKeyByChannel(interaction.channel?.id!));
    if(userToD && obj){
      let member = obj.members.filter(member => member.id == userToD?.id);
      if(member.size >= 0){
        member.at(0)?.voice.setChannel(null);
        interaction.reply({content: `${(member.at(0)!.nickname) ? member.at(0)!.nickname: userToD.username} has been disconnected!`});
      } else{
        interaction.reply({content: "User isn't here!"});
      }
    }
  }
});

client.login(process.env.THE_HEAD_TOKEN);