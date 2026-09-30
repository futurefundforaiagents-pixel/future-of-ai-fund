@echo off
REM Create USDC Token Account for Future Fund
REM This script creates an Associated Token Account (ATA) to receive USDC donations

echo.
echo =====================================================
echo FUTURE FUND - CREATE USDC TOKEN ACCOUNT
echo =====================================================
echo.

REM Check if Solana CLI is installed
where solana >nul 2>nul
if errorlevel 1 (
    echo ERROR: Solana CLI not found
    echo.
    echo INSTALL SOLANA CLI:
    echo 1. Download: https://docs.solana.com/cli/install-solana-cli-tools
    echo 2. Run installer
    echo 3. Restart terminal
    echo 4. Verify: solana --version
    echo.
    pause
    exit /b 1
)

echo Solana CLI found:
solana --version
echo.

REM Set network
echo Setting network to mainnet-beta...
solana config set --url mainnet-beta
echo.

REM Show current config
echo Current Solana config:
solana config get
echo.

REM IMPORTANT: User must provide their keypair file
echo =====================================================
echo IMPORTANT - You need your keypair file!
echo =====================================================
echo.
echo Your keypair file should be at one of these locations:
echo  - %%USERPROFILE%%\.config\solana\id.json (default)
echo  - C:\Users\YourUsername\.config\solana\id.json
echo  - ~/solana-wallet.json (if you created custom)
echo.
echo If you don't have it, create one with:
echo  $ solana-keygen new
echo.

set /p KEYPAIR="Enter path to your keypair file (press Enter for default ~/.config/solana/id.json): "

if "%KEYPAIR%"=="" (
    set KEYPAIR=%USERPROFILE%\.config\solana\id.json
)

if not exist "%KEYPAIR%" (
    echo.
    echo ERROR: Keypair file not found: %KEYPAIR%
    echo.
    echo Create a new keypair:
    echo  $ solana-keygen new -o ~/solana-wallet.json
    echo.
    pause
    exit /b 1
)

echo Using keypair: %KEYPAIR%
echo.

REM Create the USDC token account
echo =====================================================
echo CREATING USDC TOKEN ACCOUNT...
echo =====================================================
echo.
echo This will:
echo  1. Create a new token account on Solana
echo  2. Cost ~0.002 SOL (you have 0.126 SOL, so plenty!)
echo  3. Link it to your wallet
echo  4. Allow you to receive USDC donations
echo.

echo Command:
echo spl-token create-account EPjFWaJwJqkKJkx9pKrFv82bABmJVWqhxzVNMmRWt9qz ^
echo   --owner 3s47P8FgyPzHhX9srpp1eYirVAWkmyJvsPyehDmDYogP ^
echo   --fee-payer "%KEYPAIR%"
echo.

pause

echo Executing...
spl-token create-account EPjFWaJwJqkKJkx9pKrFv82bABmJVWqhxzVNMmRWt9qz ^
  --owner 3s47P8FgyPzHhX9srpp1eYirVAWkmyJvsPyehDmDYogP ^
  --fee-payer "%KEYPAIR%"

if errorlevel 1 (
    echo.
    echo ERROR: Failed to create account
    echo.
    echo Possible issues:
    echo  1. Keypair file not found or invalid
    echo  2. Wallet has no SOL for fees
    echo  3. Network connection issue
    echo  4. Account may already exist
    echo.
    pause
    exit /b 1
)

echo.
echo =====================================================
echo SUCCESS! USDC ACCOUNT CREATED
echo =====================================================
echo.

REM Verify the account was created
echo Verifying token accounts...
spl-token accounts --owner 3s47P8FgyPzHhX9srpp1eYirVAWkmyJvsPyehDmDYogP

echo.
echo =====================================================
echo NEXT STEPS
echo =====================================================
echo.
echo Your wallet is now READY to receive USDC donations!
echo.
echo Share this address with agents:
echo   3s47P8FgyPzHhX9srpp1eYirVAWkmyJvsPyehDmDYogP
echo.
echo You can now:
echo  1. Share wallet address to receive donations
echo  2. Monitor incoming donations with agent
echo  3. Withdraw to exchange when ready
echo.
echo View on Solscan:
echo   https://solscan.io/account/3s47P8FgyPzHhX9srpp1eYirVAWkmyJvsPyehDmDYogP
echo.

pause
