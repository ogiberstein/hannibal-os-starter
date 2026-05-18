# Backup and Restore

A useful backup plan distinguishes public templates from private runtime state.

## Back up

- deployment repo commit SHA
- local config with secrets handled by a secret manager
- profile router with raw IDs redacted before sharing
- runtime version or package reference
- project docs and decision logs

## Do not commit

- secret archives
- raw `.env`
- live sessions
- memories
- logs
- transcripts
- database files
- backups containing private IDs or credentials

## Restore drill

A restore drill should prove that a fresh host can recreate the runtime boundary without needing private data in the public starter repo.
