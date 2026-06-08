# ANVIL CI/CD Agent

Este é um agente simples para automatizar processos do ANVIL via GitHub Actions.

## O que ele faz

1. **Verifica builds** - Confirma que o APK foi gerado corretamente
2. **Faz QA automático** - Executa testes e verifica resultados
3. **Cria relatórios** - Gera sumários de builds

## Uso no GitHub Actions

O workflow `.github/workflows/ci.yml` já integra este agente.

## Status do Agente

O agente está em versão Beta. Funcionalidades futuras:

- [ ] Verificar APKs assinados
- [ ] Testar em múltiplas plataformas
- [ ] Análise de segurança avançada
- [ ] Geração automática de changelog
- [ ] Notificações automáticas

## Desenvolvimento

Para testar localmente:

```bash
cd tests
python test_anvil.py
```

## Contribuir

1. Fork o repo
2. Adicione seus testes em `tests/test_anvil.py`
3. Faça PR com descrição clara
4. CI/CD vai verificar automaticamente