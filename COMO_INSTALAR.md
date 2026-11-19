# Perfil GitHub — Bruno Bibiano | Cybersecurity

Este pacote substitui a apresentação antiga por um README animado com foco em segurança da informação, auditoria e defesa cibernética. Foi pensado para o repositório de perfil **BrunoBibiano/BrunoBibiano**.

## Conteúdo

- `README.md`: página do perfil, pronta para uso no GitHub.
- `assets/hero.gif`: hero animado com escudo futurista original.
- `assets/background.gif`: formação e experiência profissional.
- `assets/projects.gif`: três cards de projetos **EM BREVE**, sem fingir que já existem.
- `assets/languages.gif`: linguagens e tecnologias em aprendizado.
- `assets/radar.gif`: cabeçalho animado do radar de notícias.
- `assets/news-1.gif`, `news-2.gif`, `news-3.gif`: cards de notícias clicáveis, com animação.
- `assets/footer.gif`: rodapé com equalizador animado.
- `news.json`: últimas manchetes selecionadas, com fontes e datas.
- `scripts/update_news.py`: atualizador que lê o RSS de BleepingComputer e refaz os três cards e links.
- `.github/workflows/update-cyber-news.yml`: execução do atualizador duas vezes ao dia pelo GitHub Actions.

## Instalar pelo navegador

1. Abra https://github.com/BrunoBibiano/BrunoBibiano
2. Extraia o arquivo ZIP **perfil-github-bruno-cyber.zip** no seu computador.
3. No repositório, acesse **Add file > Upload files**.
4. Envie o `README.md` e as pastas `assets`, `scripts` e `.github` (inclusive as subpastas). Envie também `news.json`. Os caminhos das pastas devem ser preservados na raiz.
5. Confirme em **Commit changes**. Se já houver um README, substitua o arquivo anterior.
6. Abra seu perfil https://github.com/BrunoBibiano e confira os GIFs.

Se o navegador não preservar subpastas ao enviá-las, use Git no computador ou o editor do GitHub para criar os caminhos corretamente.

## Instalar via Git (alternativa mais confiável)

Com Git instalado, clone seu repositório de perfil e copie para a raiz dele **o conteúdo** da pasta extraída:

```bash
git clone https://github.com/BrunoBibiano/BrunoBibiano.git
cd BrunoBibiano
# copie aqui os arquivos e pastas do pacote extraído
git add README.md assets/ scripts/ .github/ news.json
git commit -m "feat: novo perfil de ciberseguranca animado"
git push
```

## Ativar atualização automática de notícias

1. Abra o repositório e vá em **Settings > Actions > General**.
2. Em **Workflow permissions**, selecione **Read and write permissions**, se sua conta e políticas do repositório permitirem.
3. Acesse **Actions > Atualizar radar de ciberseguranca > Run workflow** para testar.
4. Depois de ativado, o agendamento tenta atualizar o radar **duas vezes por dia** (10:17 e 22:17 UTC), sujeito a atrasos do GitHub.
5. Se o RSS externo estiver indisponível, a execução pode falhar e os cards anteriores permanecerão publicados. Os textos exibem a data da última seleção, não prometem atualização em tempo real.

Os títulos obtidos automaticamente são preservados no idioma da fonte (normalmente inglês). As notícias iniciais, selecionadas manualmente em 18/11/2026, aparecem em português.

## Personalizar

- Para alterar textos e a composição dos GIFs, edite `build_assets.py` e regenere com `python build_assets.py`. Esse script usa Pillow e um fundo original em `assets/cyber-shield-source.png`. Esses arquivos editáveis estão no pacote de fontes opcionais, não são necessários no GitHub.
- Para mudar os títulos das notícias iniciais, edite `news.json` e execute `python scripts/update_news.py --seed` (Pillow instalado).
- Para atualizar a cadência, altere `schedule.cron` no workflow.
- Para publicar um projeto de verdade no futuro, substitua o painel `projects.gif` por novos cards e links, mantendo a mesma linguagem visual.

## Limitações honestas do GitHub

O GitHub **não executa JavaScript nem permite CSS livre** dentro do README. Por isso, as animações são GIFs; não há um site completo nem efeitos de hover verdadeiros. Os cards de notícias são clicáveis, mas a mudança dos artigos depende de GitHub Actions, RSS e permissão de escrita. No celular, as imagens são reduzidas à largura disponível.

Todos os textos essenciais de apresentação também estão disponíveis no README em texto acessível no bloco "Conheça minha trajetória profissional".
