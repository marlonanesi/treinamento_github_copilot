# Guia rápido: instalar o GitHub Copilot (VS Code e Visual Studio)

Este guia direto ao ponto mostra como instalar e ativar o GitHub Copilot no VS Code e no Visual Studio, com notas rápidas por sistema operacional (Windows, macOS e Linux) e dicas de solução de problemas.

## Checklist do que você fará

- Verificar pré-requisitos (conta/licença e versão do editor)
- Instalar a extensão (VS Code) ou o componente (Visual Studio)
- Entrar com sua conta GitHub e ativar o Copilot
- Fazer um teste rápido de sugestão
- Ajustar configurações úteis e tratar eventuais bloqueios de rede

---

## Pré-requisitos

- Conta GitHub com acesso ao Copilot (assinatura individual, equipe/empresa ou isenção para estudantes/educadores/maintainers). Se estiver numa organização, confirme se a política permite o uso do Copilot.
- Conexão de rede permitindo acesso aos domínios do Copilot: `api.githubcopilot.com`, `*.github.com`, `*.githubusercontent.com`, e `copilot-proxy.githubusercontent.com` (firewall/proxy não devem inspecionar TLS nesses domínios).
- Editor atualizado:
	- VS Code: versão atual estável.
	- Visual Studio 2022: atualizado (recomendado 17.6+ para Copilot Chat).

---

## Instalação no VS Code

1) Instalar extensões

- Pela UI: abra o VS Code > Extensions (Ctrl+Shift+X) > procure por “GitHub Copilot” e “GitHub Copilot Chat” > Install.
- Pela linha de comando:

	- Windows (PowerShell):

		```powershell
		code --install-extension GitHub.copilot
		code --install-extension GitHub.copilot-chat
		```

	- macOS/Linux (Terminal):

		```bash
		code --install-extension GitHub.copilot
		code --install-extension GitHub.copilot-chat
		```

	Observações:
	- Se o comando `code` não funcionar no macOS, rode no VS Code: Command Palette > “Shell Command: Install 'code' command in PATH”. No Windows, o instalador normalmente adiciona o `code` ao PATH; se não, reinstale o VS Code marcando a opção “Add to PATH”.

2) Entrar e ativar

- Na barra inferior, clique em “Sign in to GitHub” (ou abra a Command Palette e procure por “GitHub: Sign in”). Conclua o login no navegador e volte ao VS Code.
- Verifique o status do Copilot: Command Palette > “Copilot: Toggle” (deve ficar “Enabled”).

3) Teste rápido

- Abra um arquivo de código e digite um comentário, por exemplo:

	```python
	# função para inverter uma string
	```

	Aguarde a sugestão inline. Aceite com Tab (ou ajuste a tecla em Settings > Copilot).

4) Configurações úteis (Settings > “Copilot”)

- Ativar/Desativar sugestões inline por linguagem
- Filtrar trechos semelhantes a código público (Public Code Filter)
- Mostrar explicações e chat no painel lateral (Copilot Chat)

### Notas por sistema operacional (VS Code)

- Windows
	- PowerShell/CLI funcionam normalmente com o `code`. Em ambientes corporativos, verifique proxy do sistema e variáveis de ambiente.
	- WSL: ao abrir uma pasta WSL, instale o Copilot também no ambiente remoto quando o VS Code solicitar.

- macOS
	- Habilite o comando `code` via Command Palette (ver acima) se quiser instalar extensões por terminal.
	- Pop-ups do Keychain podem aparecer no primeiro login; aceite para guardar credenciais.

- Linux
	- Para salvar credenciais, alguns distros precisam do `libsecret`. Exemplos:

		```bash
		# Debian/Ubuntu
		sudo apt-get update && sudo apt-get install -y libsecret-1-0

		# Fedora
		sudo dnf install -y libsecret

		# Arch
		sudo pacman -S --noconfirm libsecret
		```

	- Se usar container/Dev Container, instale as extensões também no container quando o VS Code sugerir.

---

## Instalação no Visual Studio 2022

1) Instalar o GitHub Copilot

- Abra o Visual Studio 2022 > menu Extensions > Manage Extensions > pesquise “GitHub Copilot” > Download/Install. Reinicie o Visual Studio quando solicitado.
- Para Copilot Chat, instale também “GitHub Copilot Chat” (requer VS 17.6+).

2) Entrar e ativar

- Após reiniciar, vá em View > Other Windows > GitHub e entre com sua conta GitHub se o prompt não aparecer automaticamente.
- Verifique se o Copilot está habilitado em Tools > Options > GitHub Copilot.

3) Teste rápido

- Abra um arquivo de código, comece a digitar um comentário descritivo e observe as sugestões inline. Aceite com Tab (ou conforme o mapeamento de teclas do VS).

### Notas por sistema operacional (Visual Studio)

- Windows (nativo)
	- Visual Studio é suportado no Windows. Se estiver atrás de proxy corporativo, ajuste em Tools > Options > Environment > Web Proxy ou use o proxy do sistema.
	- Firewalls com inspeção TLS podem bloquear autenticação/sugestões; peça exceção para os domínios listados em Pré-requisitos.

- macOS/Linux
	- Visual Studio para Mac foi descontinuado; use VS Code nessas plataformas.

---

## Rede e Proxy (dicas rápidas)

- VS Code: Settings > “Proxy” (HTTP: Proxy) ou use variáveis de ambiente:

	- Windows (PowerShell):

		```powershell
		$env:HTTP_PROXY = "http://usuario:senha@proxy.exemplo:8080"
		$env:HTTPS_PROXY = "http://usuario:senha@proxy.exemplo:8080"
		```

	- macOS/Linux:

		```bash
		export HTTP_PROXY=http://usuario:senha@proxy.exemplo:8080
		export HTTPS_PROXY=http://usuario:senha@proxy.exemplo:8080
		```

- Certifique-se de que inspeção SSL/TLS não esteja ativa para os domínios do Copilot.

---

## Verificações e troubleshooting

- Conferir se as extensões estão instaladas (VS Code):

	- Windows (PowerShell):

		```powershell
		code --list-extensions | Select-String copilot
		```

	- macOS/Linux:

		```bash
		code --list-extensions | grep -i copilot
		```

- Loop de login ou autorização falha
	- Saia e entre novamente na conta GitHub pelo editor.
	- Apague sessões antigas (VS Code: Accounts > Sign Out; também confira Settings Sync se estiver ativo).
	- No Linux, confirme a instalação do `libsecret`.

- Sem sugestões
	- Verifique se o Copilot está “Enabled”.
	- Abra um arquivo suportado (ex.: .py, .ts, .js, .cs, .java).
	- Cheque a conectividade com `api.githubcopilot.com` (proxy/firewall).

- Ambiente corporativo
	- Confirme se sua organização/empresa atribuiu uma licença Copilot ao seu usuário.
	- Se a política da org exigir, ative o filtro de código público nas configurações do Copilot.

---

## Dicas finais

- Combine Copilot (sugestões inline) com Copilot Chat para perguntas, geração e explicação de código.
- Ajuste a granularidade das sugestões por linguagem para reduzir “ruído” em arquivos onde você não deseja autocompletar agressivo.
- Em projetos remotos (WSL, containers, SSH), instale as extensões também no “lado remoto” quando o VS Code solicitar.

---

## Referências rápidas

- Extensões (VS Code): “GitHub Copilot” e “GitHub Copilot Chat”
- Visual Studio 2022: Extensions > Manage Extensions > GitHub Copilot / Copilot Chat
- Domínios a liberar: `api.githubcopilot.com`, `*.github.com`, `*.githubusercontent.com`, `copilot-proxy.githubusercontent.com`

Se precisar, peça um checklist de diagnóstico mais detalhado (rede, proxy, licenças e versões).

