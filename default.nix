with import <nixpkgs> {};

(pkgs.python36.withPackages (
  pkgs: [
    pkgs.urwid
    pkgs.black
    pkgs.tqdm
  ])
).env

