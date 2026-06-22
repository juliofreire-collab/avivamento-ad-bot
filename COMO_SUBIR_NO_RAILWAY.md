# 🚀 Como Subir o Bot no Railway (GRATUITO - 24/7)

## O que é o Railway?
Railway é um serviço de hospedagem na nuvem que mantém seu bot rodando **24 horas por dia, 7 dias por semana**, mesmo quando você fechar o celular ou o computador.

---

## PASSO A PASSO (10 minutos)

### PASSO 1 — Crie sua conta no Railway
1. Acesse: **https://railway.app**
2. Clique em **"Login"**
3. Escolha **"Login with GitHub"**
4. Se não tem GitHub, crie em: https://github.com — é gratuito

### PASSO 2 — Baixe os arquivos do bot
1. Aqui no Replit, clique nos **3 pontinhos** no topo
2. Clique em **"Download as zip"**
3. Salve o arquivo no seu celular ou computador

### PASSO 3 — Crie um repositório no GitHub
1. Acesse: **https://github.com/new**
2. Nome do repositório: `avivamento-bot`
3. Deixe como **Privado (Private)**
4. Clique em **"Create repository"**
5. Faça upload dos arquivos da pasta `artifacts/telegram-bot/`

### PASSO 4 — Conecte ao Railway
1. No Railway, clique em **"New Project"**
2. Escolha **"Deploy from GitHub repo"**
3. Selecione o repositório `avivamento-bot`
4. O Railway vai detectar automaticamente que é Python

### PASSO 5 — Configure as variáveis de ambiente
No Railway, vá em **"Variables"** e adicione:

| Variável | Valor |
|----------|-------|
| `BOT_TOKEN` | `8981755295:AAF_BaXcWlUuasIfDoao3787lJNMJMCiUd4` |
| `CHANNEL_ID` | `@avivamentoad` |
| `GROUP_ID` | `-1002695823149` |
| `OWNER_ID` | `SEU_ID_DO_TELEGRAM` |

**Como descobrir seu OWNER_ID:**
- Fale com o bot @userinfobot no Telegram
- Ele vai te enviar seu ID numérico

### PASSO 6 — Deploy!
1. Clique em **"Deploy"**
2. Aguarde 2-3 minutos
3. O bot vai aparecer como **"Active"** ✅

---

## ✅ Como saber se está funcionando?
- No Railway, o status vai mostrar **"Active"** em verde
- Envie `/start` para o bot no Telegram
- Ele deve responder imediatamente

---

## 💾 Importante: Persistência de dados
O Railway tem armazenamento temporário. Para os vídeos e imagens que você enviar ao bot **não se perderem** quando o serviço reiniciar, recomendo adicionar um **Volume** no Railway:

1. No Railway, clique em **"+ New"** → **"Volume"**
2. Monte no caminho: `/app`
3. Isso garante que `media_storage.json` seja salvo permanentemente

---

## 📱 Comandos do Bot

### Para você (dono):
- Envie **vídeos ou imagens** no privado do bot para salvar para postagem
- `/postar_versiculo` — Posta versículo no canal agora
- `/postar_midia` — Posta uma mídia salva no canal agora
- `/status` — Ver estatísticas
- `/listar_midia` — Quantas mídias estão salvas
- `/banir` — Banir usuário (responda a mensagem dele)
- `/silenciar` — Silenciar usuário
- `/liberar` — Liberar usuário
- `/anuncio [texto]` — Fazer anúncio no grupo
- `/fixar` — Fixar mensagem

### Para todos:
- `/versiculo` — Receber versículo com imagem
- `/regras` — Ver regras do grupo
- `/ajuda` — Ver todos os comandos

---

## ⏰ Posts automáticos configurados:
- **07h, 13h e 21h** → Versículo com imagem no canal
- **09h e 19h** → Sua mídia (vídeo ou imagem) no canal
- **07h, 13h e 21h** → Mensagem bíblica no grupo
- **A cada 4 horas** → Regras postadas no grupo

---

## 🆘 Problemas?
Se o bot parar, no Railway clique em **"Redeploy"** e ele volta em segundos.

Que Deus abençoe este ministério! 🙏✝️
